from kivy.input.motionevent import MotionEvent
from kivy.properties import ColorProperty, ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget

from hanako.app.uix.behaviors import HoverBehavior


class MangaDetail(ButtonBehavior, HoverBehavior, Widget):
    thumbnail = StringProperty("resources/drawables/icon_image.png")
    title = StringProperty()
    color = ColorProperty()
    color_normal = ColorProperty((0.0, 0.0, 0.0, 0.3))
    color_hover = ColorProperty((0.0, 0.0, 0.0, 0.7))
    color_down = ColorProperty((0.0, 0.0, 0.0, 0.7))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.color = self.color_normal

    def on_mouse_enter(self, mouse_pos: ObjectProperty) -> None:
        self.color = self.color_hover or self.color

        super().on_mouse_enter(mouse_pos)

    def on_mouse_leave(self) -> None:
        if self.state == "normal":
            self.color = self.color_normal

        super().on_mouse_leave()

    def on_touch_down(self, touch: MotionEvent) -> bool:
        self.color = self.color_down or self.color

        return super().on_touch_down(touch)

    def on_touch_up(self, touch: MotionEvent) -> bool:
        if self.hovering:
            self.color = self.color_hover or self.color
        else:
            self.color = self.color_normal

        return super().on_touch_up(touch)

    def on_press(self) -> None:
        ...

    def on_release(self) -> None:
        ...
