from kivy.input.motionevent import MotionEvent
from kivy.properties import ColorProperty, ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from hanako.app.uix.behaviors import HoverBehavior


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    color_normal = ColorProperty((1, 1, 1, 1))
    color_hover = ColorProperty(None)
    color_down = ColorProperty(None)
    source_normal = StringProperty("atlas://data/images/defaulttheme/button")
    source_hover = StringProperty(None)
    source_down = StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.color = self.color_normal
        self.source = self.source_normal

    def on_mouse_enter(self: Image, mouse_pos: ObjectProperty) -> None:
        self.color = self.color_hover or self.color
        self.source = self.source_hover or self.source

        super().on_mouse_enter(mouse_pos)

    def on_mouse_leave(self: Image) -> None:
        if self.state == "normal":
            self.color = self.color_normal
            self.source = self.source_normal

        super().on_mouse_leave()

    def on_touch_down(self: Image, touch: MotionEvent) -> bool:
        self.color = self.color_down or self.color
        self.source = self.source_down or self.source

        return super().on_touch_down(touch)

    def on_touch_up(self: Image, touch: MotionEvent) -> bool:
        if self.hovering:
            self.color = self.color_hover or self.color
            self.source = self.source_hover or self.source
        else:
            self.color = self.color_normal
            self.source = self.source_normal

        return super().on_touch_up(touch)

    def on_press(self) -> None:
        ...

    def on_release(self) -> None:
        ...
