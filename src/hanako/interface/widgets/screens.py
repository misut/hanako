from collections.abc import Callable

from kivy.effects.scroll import ScrollEffect
from kivy.graphics.svg import Svg
from kivy.metrics import dp
from kivy.properties import Property
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scatterlayout import Scatter, ScatterLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget


class SvgWidget(Scatter):
    def __init__(self, source: str, scale: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self._svg = Svg(source=source, color=(0, 0, 0, 1))

        self.scale_to(scale)

    def scale_to(self, val: float) -> None:
        self.scale = val
        self.size = self._svg.width, self._svg.height


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


class MainScreen(Screen):
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

            layout = ScatterLayout(size_hint=(None, None))
            layout.bind(pos=fit_into_parent(0.0, 1.0, dp(60), 0.0))
            self.add_widget(layout)
            print(f"layout size: {layout.size}")

            home = SvgWidget(
                source="resources/icon_home.svg",
                pos=(dp(16), layout.height - dp(46)),
            )
            home.scale_to(1.0)
            print(home.size)
            layout.add_widget(home)

            search = SvgWidget(
                source="resources/icon_search.svg",
                pos=(dp(16), layout.height - dp(102)),
            )
            search.scale_to(1.0)
            layout.add_widget(search)

    def __init__(self) -> None:
        super().__init__(name="main")

        layout = ScatterLayout(size_hint=(1.0, 1.0))
        self.add_widget(layout)

        library = MainScreen.LibraryView()
        layout.add_widget(library)

        sidebar = MainScreen.SidebarView()
        layout.add_widget(sidebar)


class ThumbnailDetailWidget(ScatterLayout):
    def __init__(self, num: int) -> None:
        super().__init__(size_hint=(1.0, 1.0))

        missing = SvgWidget(source="resources/icon_image.svg", pos=(dp(30), dp(16)))
        missing.scale_to(2.0)
        self.add_widget(missing)

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
