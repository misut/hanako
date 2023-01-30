from queue import Empty, Queue

from hanako.interfaces import Message, MessageReceiver, MessageSender
from hanako.monads import Some, Null, Option


class InMemoryMessageQueue(MessageReceiver, MessageSender):
    _queue: Queue[Message]

    def __init__(self, limit: int = 0) -> None:
        self._queue = Queue(limit)

    def send(self, message: Message) -> None:
        self._queue.put(message)

    def receive(self, timeout: float | None = None) -> Option[Message]:
        try:
            message = self._queue.get(block=False, timeout=timeout)
            return Some(message)
        except Empty:
            return Null
