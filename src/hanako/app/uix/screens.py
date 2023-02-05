from collections.abc import Callable

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ReferenceListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from hanako.app.uix.behaviors import CommandBehavior
from hanako.app.uix.image_button import ImageButton
from hanako.command import commands


def size_to_parent(
    widget: Widget,
    ratio_width: float = 1.0,
    ratio_height: float = 1.0,
    offset_width: float = 0.0,
    offset_height: float = 0.0,
) -> Callable[[Widget, ReferenceListProperty], None]:
    def resize(*_) -> None:
        widget.width = widget.parent.width * ratio_width + offset_width
        widget.height = widget.parent.height * ratio_height + offset_height

    return resize


def pos_to_parent(
    widget: Widget,
    ratio_x: float = 0.0,
    ratio_y: float = 0.0,
    offset_x: float = 0.0,
    offset_y: float = 0.0,
) -> Callable[[Widget, ReferenceListProperty], None]:
    def repos(*_) -> None:
        widget.x = widget.parent.width * ratio_x + offset_x
        widget.y = widget.parent.height * ratio_y + offset_y

    return repos


class MainScreen(Screen):
    def __init__(self) -> None:
        super().__init__(name="home")

        layout = RelativeLayout(pos_hint={"x": 0.0, "y": 0.0}, size_hint=(1.0, 1.0))
        self.add_widget(layout)

        home = HomeView()
        layout.add_widget(home)

        sidebar = SidebarView()
        layout.add_widget(sidebar)


class HomeView(ScrollView):
    _manga_list: GridLayout

    def __init__(self) -> None:
        super().__init__(
            do_scroll=(False, True),
            pos_hint={"x": 0.0, "top": 1.0},
            size_hint=(None, None),
            scroll_wheel_distance=100,
        )
        self.bind(pos=size_to_parent(self, 1.0, 1.0, -dp(60), 0.0))

        self._layout = GridLayout(
            cols=1,
            size_hint=(1.0, None),
            row_default_height="80dp",
            row_force_default=True,
        )
        self._layout.bind(minimum_height=self._layout.setter("height"))
        self.add_widget(self._layout)

        for i in range(10):
            thumbnail = ThumbnailDetailWidget(
                title=f"Hello, world #{i}", description=f"Description - {i}"
            )
            self._layout.add_widget(thumbnail)


class SearchView(ScrollView):
    def __init__(self) -> None:
        super().__init__(
            do_scroll=(False, True),
            pos_hint={"x": 0.0, "top": 1.0},
            size_hint=(None, None),
            scroll_wheel_distance=100,
        )
        self.bind(pos=size_to_parent(self, 1.0, 1.0, -dp(60), 0.0))

        layout = RelativeLayout(pos_hint={"x": 0.0, "y": 0.0}, size_hint=(1.0, 1.0))
        self.add_widget(layout)


class SidebarView(ScrollView):
    def __init__(self) -> None:
        super().__init__(
            do_scroll=(False, True),
            pos_hint={"right": 1.0, "top": 1.0},
            size_hint=(None, 1.0),
            scroll_wheel_distance=100,
        )
        self.bind(pos=size_to_parent(self, 0.0, 1.0, dp(60), 0.0))

        layout = RelativeLayout(pos_hint={"x": 0.0, "y": 0.0}, size_hint=(1.0, 1.0))
        self.add_widget(layout)

        home_button = ImageButton(
            source_normal="resources/drawables/icon_home.png",
            allow_stretch=True,
            color_normal=(0, 0, 0, 1),
            color_hover=(0, 1, 1, 1),
            mipmap=True,
            size_hint=(None, None),
            size=(dp(24), dp(24)),
        )
        layout.bind(size=pos_to_parent(home_button, 0.0, 1.0, dp(16), -dp(48)))
        layout.add_widget(home_button)

        search_button = ImageButton(
            source_normal="resources/drawables/icon_search.png",
            allow_stretch=True,
            color_normal=(0, 0, 0, 1),
            color_hover=(0, 1, 1, 1),
            mipmap=True,
            size_hint=(None, None),
            size=(dp(24), dp(24)),
        )
        layout.bind(size=pos_to_parent(search_button, 0.0, 1.0, dp(16), -dp(96)))
        layout.add_widget(search_button)

        filter_button = ImageButton(
            source_normal="resources/drawables/icon_filter.png",
            allow_stretch=True,
            color_normal=(0, 0, 0, 1),
            color_hover=(0, 1, 1, 1),
            mipmap=True,
            size_hint=(None, None),
            size=(dp(24), dp(24)),
        )
        layout.bind(size=pos_to_parent(filter_button, 0.0, 1.0, dp(16), -dp(144)))
        layout.add_widget(filter_button)

        settings_button = ImageButton(
            source_normal="resources/drawables/icon_settings.png",
            allow_stretch=True,
            color_normal=(0, 0, 0, 1),
            color_hover=(0, 1, 1, 1),
            mipmap=True,
            pos=(dp(16), dp(16)),
            size_hint=(None, None),
            size=(dp(24), dp(24)),
        )
        layout.add_widget(settings_button)

    def on_pressed_home(self) -> None:
        print("pressed home")


class ThumbnailDetailWidget(ButtonBehavior, CommandBehavior, RelativeLayout):
    def __init__(self, title: str, description: str) -> None:
        super().__init__(size_hint=(1.0, 1.0))

        thumbnail = Image(
            source="resources/drawables/icon_image.png",
            allow_stretch=True,
            color=(0, 0, 0, 1),
            mipmap=True,
            pos=(dp(32), dp(8)),
            size_hint=(None, None),
            size=(dp(48), dp(48)),
        )
        self.add_widget(thumbnail)

        title_label = Label(
            text=title,
            color=(0, 0, 0, 1),
            font_size="17sp",
            halign="left",
            pos=(dp(108), dp(32)),
        )
        title_label.bind(size=title_label.setter("text_size"))
        self.add_widget(title_label)

        description_label = Label(
            text=description,
            color=(0, 0, 0, 1),
            font_size="14sp",
            halign="left",
            pos=(dp(108), dp(8)),
        )
        description_label.bind(size=description_label.setter("text_size"))
        self.add_widget(description_label)

    def on_press(self) -> None:
        command = commands.FetchMangaIDs(offset=0, limit=10, triggered_by="thumbnail")
        self.dispatch("on_command", command)
