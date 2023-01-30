from kivy.core.window import Window
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.widget import Widget

from hanako.drivers import Publisher
from hanako.interfaces import Message, MessageSender
from hanako.models import Command


class HoverBehavior:
    hovering = BooleanProperty(False)
    enter_point = ObjectProperty(allownone=True)

    def __init__(self: Widget, **kwargs) -> None:
        assert isinstance(self, Widget), "'HoverBehavior' should be mixin with 'Widget'"
        super().__init__(**kwargs)

        self.register_event_type("on_enter")
        self.register_event_type("on_leave")
        Window.bind(mouse_pos=self.on_mouse_update)

    def on_mouse_enter(self: Widget, mouse_pos: ObjectProperty) -> None:
        self.hovering = True
        self.enter_point = mouse_pos
        self.dispatch("on_enter")

    def on_mouse_leave(self: Widget) -> None:
        self.hovering = False
        self.enter_point = None
        self.dispatch("on_leave")

    def on_mouse_update(self: Widget, _: Window, mouse_pos: ObjectProperty) -> None:
        if not self.collide_point(*self.to_widget(*mouse_pos)):
            self.on_mouse_leave()
            return

        if self.hovering:
            return

        self.on_mouse_enter(mouse_pos)

    def on_enter(self) -> None:
        ...

    def on_leave(self) -> None:
        ...


class MessengerBehavior:
    publisher = ObjectProperty(Publisher())

    def __init__(self, **kwargs) -> None:
        assert isinstance(
            self, Widget
        ), "'MessengerBehavior' should be mixin with 'Widget'"
        assert "publisher" not in kwargs or isinstance(
            kwargs["publisher"], MessageSender
        ), "'publisher' should be an instance of 'MessageSender'"
        super().__init__(**kwargs)

        self.register_event_type("on_command")

    def on_command(self, command: Command) -> None:
        self.publisher.send(Message.from_command(command=command))
