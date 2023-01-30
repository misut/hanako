from typing import ClassVar

from hanako.drivers.in_memory_message_queue import InMemoryMessageQueue
from hanako.interfaces import Message, MessageReceiver, MessageSender
from hanako.monads import Option


class _Singleton:
    _instance: ClassVar[InMemoryMessageQueue | None] = None

    @classmethod
    def get_instance(cls) -> InMemoryMessageQueue:
        if cls._instance is None:
            cls._instance = InMemoryMessageQueue()
        return cls._instance


class Publisher(MessageSender):
    _engine: MessageSender
    _triggered_by: str

    def __init__(self, triggered_by: str = "") -> None:
        self._engine = _Singleton.get_instance()
        self._triggered_by = triggered_by

    def send(self, message: Message) -> None:
        stamped = message
        if not stamped.triggered_by:
            stamped = Message(
                type=message.type,
                data=message.data,
                occured_at=message.occured_at,
                triggered_by=self._triggered_by,
            )
        self._engine.send(stamped)


class Subscriber(MessageReceiver):
    _engine: MessageReceiver

    def __init__(self) -> None:
        self._engine = _Singleton.get_instance()

    def receive(self, timeout: float | None = None) -> Option[Message]:
        return self._engine.receive(timeout)
