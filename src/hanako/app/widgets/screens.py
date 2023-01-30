from collections.abc import Callable

from kivy.core.window import Window
from kivy.effects.scroll import ScrollEffect
from kivy.metrics import dp
from kivy.properties import Property
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from hanako.app.widgets.base import MessageDispatcher
from hanako.command import commands


def fit_into_parent(
    ratio_width: float = 1.0,
    ratio_height: float = 1.0,
    offset_width: float = 0.0,
    offset_height: float = 0.0,
) -> Callable[[Widget, Property], None]:
    def resize(instance: Widget, _: Property) -> None:
        instance.width = instance.parent.width * ratio_width + offset_width
        instance.height = instance.parent.height * ratio_height + offset_height

    return resize


class HomeScreen(Screen):
    class LibraryView(ScrollView):
        def __init__(self) -> None:
            super().__init__(
                do_scroll=(False, True),
                pos_hint={"x": 0.0, "top": 1.0},
                size_hint=(None, None),
                scroll_wheel_distance=100,
            )
            self.bind(pos=fit_into_parent(1.0, 1.0, -dp(60), 0.0))

            layout = GridLayout(
                cols=1,
                size_hint=(1.0, None),
                row_default_height="80dp",
                row_force_default=True,
            )
            layout.bind(minimum_height=layout.setter("height"))
            self.add_widget(layout)

            for i in range(10):
                thumbnail = ThumbnailDetailWidget(i)
                layout.add_widget(thumbnail)

    class SidebarView(ScrollView):
        def __init__(self) -> None:
            super().__init__(
                do_scroll=(False, True),
                effect_cls=ScrollEffect,
                pos_hint={"right": 1.0, "top": 1.0},
                size_hint=(None, None),
                scroll_wheel_distance=100,
            )
            self.bind(pos=fit_into_parent(0.0, 1.0, dp(60), 0.0))

            layout = RelativeLayout(pos_hint={"x": 0.0, "y": 0.0}, size_hint=(1.0, 1.0))
            self.add_widget(layout)

            home_button = Image(
                source="resources/drawables/icon_home.png",
                allow_stretch=True,
                color=(0, 0, 0, 1),
                mipmap=True,
                pos=(dp(16), Window.height - dp(48)),
                size_hint=(None, None),
                size=(dp(24), dp(24)),
            )
            layout.add_widget(home_button)

            search_button = Image(
                source="resources/drawables/icon_search.png",
                allow_stretch=True,
                color=(0, 0, 0, 1),
                mipmap=True,
                pos=(dp(16), layout.height - dp(96)),
                size_hint=(None, None),
                size=(dp(24), dp(24)),
            )
            layout.add_widget(search_button)

            filter_button = Image(
                source="resources/drawables/icon_filter.png",
                allow_stretch=True,
                color=(0, 0, 0, 1),
                mipmap=True,
                pos=(dp(16), layout.height - dp(144)),
                size_hint=(None, None),
                size=(dp(24), dp(24)),
            )
            layout.add_widget(filter_button)

            settings_button = Image(
                source="resources/drawables/icon_settings.png",
                allow_stretch=True,
                color=(0, 0, 0, 1),
                mipmap=True,
                pos=(dp(16), dp(16)),
                size_hint=(None, None),
                size=(dp(24), dp(24)),
            )
            layout.add_widget(settings_button)

    def __init__(self) -> None:
        super().__init__(name="home")

        layout = RelativeLayout(pos_hint={"x": 0.0, "y": 0.0}, size_hint=(1.0, 1.0))
        self.add_widget(layout)

        library = HomeScreen.LibraryView()
        layout.add_widget(library)

        sidebar = HomeScreen.SidebarView()
        layout.add_widget(sidebar)


class ThumbnailDetailWidget(ButtonBehavior, MessageDispatcher, RelativeLayout):
    thumbnail: Image

    def __init__(self, num: int) -> None:
        super().__init__(size_hint=(1.0, 1.0))

        self.thumbnail = Image(
            source="resources/drawables/icon_image.png",
            allow_stretch=True,
            color=(0, 0, 0, 1),
            mipmap=True,
            pos=(dp(32), dp(8)),
            size_hint=(None, None),
            size=(dp(48), dp(48)),
        )
        self.add_widget(self.thumbnail)

        title = Label(
            text=f"Hello, world! #{num}",
            color=(0, 0, 0, 1),
            font_size="17sp",
            halign="left",
            pos=(dp(108), dp(32)),
        )
        title.bind(size=title.setter("text_size"))
        self.add_widget(title)

        description = Label(
            text=f"Description #{num}",
            color=(0, 0, 0, 1),
            font_size="14sp",
            halign="left",
            pos=(dp(108), dp(8)),
        )
        description.bind(size=description.setter("text_size"))
        self.add_widget(description)

    def on_press(self) -> None:
        command = commands.FetchMangaIDs(offset=0, limit=10, triggered_by="thumbnail")
        self.dispatch("on_command", command)
