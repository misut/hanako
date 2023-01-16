from kivy.uix.actionbar import (ActionBar, ActionButton, ActionPrevious,
                                ActionView)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView


class MainWidget(BoxLayout):
    def __init__(self) -> None:
        super().__init__(orientation="vertical", size_hint=(1.0, 1.0))

        search_bar = SearchWidget()
        self.add_widget(search_bar, index=1)

        library = LibraryWidget()
        self.add_widget(library, index=0)


class SearchWidget(ActionBar):
    def __init__(self) -> None:
        super().__init__()

        action_view = ActionView()
        self.add_widget(action_view)

        action_previous = ActionPrevious(title="Hello, world!")
        action_view.add_widget(action_previous)

        search_button = ActionButton(text="Go")
        action_view.add_widget(search_button)


class LibraryWidget(ScrollView):
    layout: GridLayout

    def __init__(self) -> None:
        super().__init__(size_hint=(1.0, 0.95), scroll_wheel_distance=100)

        self.layout = GridLayout(
            cols=1,
            size_hint=(1.0, None),
            row_default_height="120dp",
            row_force_default=True,
        )
        self.layout.bind(minimum_height=self.layout.setter("height"))
        self.add_widget(self.layout)

        for i in range(10):
            thumbnail = ThumbnailDetailWidget(i)
            self.layout.add_widget(thumbnail)


class ThumbnailDetailWidget(RelativeLayout):
    def __init__(self, num: int) -> None:
        super().__init__(size_hint_x=1.0, height="60dp")

        missing = Image(
            source="resources/missing.png",
            size_hint=(0.3, 1.0),
            pos_hint={"x": 0.0, "y": 0.0},
        )
        self.add_widget(missing)

        title = Label(
            text=f"Hello, world! #{num}",
            size_hint=(0.7, 0.5),
            pos_hint={"x": 0.3, "y": 0.5},
            font_size="17sp",
            halign="left",
        )
        title.bind(size=title.setter("text_size"))
        self.add_widget(title)

        description = Label(
            text=f"Description #{num}",
            size_hint=(0.7, 0.5),
            pos_hint={"x": 0.3, "y": 0.2},
            font_size="14sp",
            halign="left",
        )
        description.bind(size=description.setter("text_size"))
        self.add_widget(description)
