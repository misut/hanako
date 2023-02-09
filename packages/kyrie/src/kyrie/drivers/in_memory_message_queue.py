from queue import Empty, Queue

from kyrie.interfaces import Message, Receiver, Sender
from kyrie.monads import Null, Option, Some


class InMemoryMessageQueue(Receiver, Sender):
    _queue: Queue[Message]

    def __init__(self, limit: int = 0) -> None:
        self._queue = Queue(limit)

    async def send(self, message: Message) -> None:
        self._queue.put_nowait(message)

    async def receive(self, timeout: float | None = None) -> Option[Message]:
        try:
            message = self._queue.get_nowait()
            return Some(message)
        except Empty:
            return Null
