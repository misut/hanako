from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import ObservableReferenceList
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget

from hanako.interface import widgets


class MainApp(App):
    def build(self) -> ScreenManager:
        Window.borderless = False

        screen_manager = ScreenManager()
        screen_manager.add_widget(widgets.MainScreen())
        screen_manager.bind(pos=self._update_rect, size=self._update_rect)

        with screen_manager.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=screen_manager.size)

        return screen_manager

    def _update_rect(self, instance: Widget, _: ObservableReferenceList) -> None:
        self.rect.pos = instance.pos
        self.rect.size = instance.size
