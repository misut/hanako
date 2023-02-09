from typing import ClassVar

from kyrie.drivers.in_memory_message_queue import InMemoryMessageQueue
from kyrie.interfaces import Message, Receiver, Sender
from kyrie.monads import Option


class _Singleton:
    _instance: ClassVar[InMemoryMessageQueue | None] = None

    @classmethod
    def get_instance(cls) -> InMemoryMessageQueue:
        if cls._instance is None:
            cls._instance = InMemoryMessageQueue()
        return cls._instance


class Publisher(Sender):
    _engine: Sender
    _triggered_by: str

    def __init__(self, engine: Sender | None = None, triggered_by: str = "") -> None:
        self._engine = engine or _Singleton.get_instance()
        self._triggered_by = triggered_by

    async def send(self, message: Message) -> None:
        stamped = message
        if not stamped.triggered_by:
            stamped = Message(
                type=message.type,
                data=message.data,
                occured_at=message.occured_at,
                triggered_by=self._triggered_by,
            )
        await self._engine.send(stamped)


class Subscriber(Receiver):
    _engine: Receiver

    def __init__(self, engine: Receiver | None = None) -> None:
        self._engine = engine or _Singleton.get_instance()

    async def receive(self, timeout: float | None = None) -> Option[Message]:
        return await self._engine.receive(timeout)
