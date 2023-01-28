from queue import Empty, Queue

from hanako.interfaces import Message, Receiver, Sender
from hanako.monads import SOME, NONE, Option


class InMemoryMessageQueue(Receiver, Sender):
    _queue: Queue[Message]

    def __init__(self, limit: int = 0) -> None:
        self._queue = Queue(limit)

    def send(self, message: Message) -> None:
        self._queue.put(message)

    def receive(self, timeout: float | None = None) -> Option[Message]:
        try:
            message = self._queue.get(block=False, timeout=timeout)
            return SOME(message)
        except Empty:
            return NONE
