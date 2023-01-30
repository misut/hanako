from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget

from hanako.app.uix.screens import MainScreen


class RootWidget(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(MainScreen())
        self.bind(size=self.update_background)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size)

    def update_background(self, widget: Widget, _) -> None:
        self.rect.pos = widget.pos
        self.rect.size = widget.size
