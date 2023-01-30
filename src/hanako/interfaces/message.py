import abc
from datetime import datetime
from typing import final

from hanako.models import Command, DefaultDatetimeField, ImmutableModel
from hanako.monads import Option


@final
class Message(ImmutableModel):
    type: str
    data: str
    occured_at: datetime = DefaultDatetimeField
    triggered_by: str = ""

    class Config:
        extra = "ignore"

    @classmethod
    def from_command(cls, command: Command) -> "Message":
        return cls(
            type=command.__class__.__name__,
            data=command.json(),
            triggered_by=command.triggered_by,
        )


class MessageSender(abc.ABC):
    @abc.abstractmethod
    def send(self, message: Message) -> None:
        ...


class MessageReceiver(abc.ABC):
    @abc.abstractmethod
    def receive(self, timeout: float | None = None) -> Option[Message]:
        ...
