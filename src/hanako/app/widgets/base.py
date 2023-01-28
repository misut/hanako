from kivy.event import EventDispatcher

from hanako.drivers import Publisher
from hanako.interfaces import Message, Sender
from hanako.models import Command


class MessageDispatcher(EventDispatcher):
    _publisher: Sender

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self._publisher = Publisher()
        self.register_event_type("on_command")

    def on_command(self, command: Command) -> None:
        assert self._publisher
        self._publisher.send(Message.from_command(command=command))
