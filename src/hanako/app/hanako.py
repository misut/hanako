import asyncio

from kivy.app import App
from loguru import logger

from hanako.app import uix
from hanako.command import CommandContext, command_handler, commands
from hanako.interfaces import Message, MessageReceiver

INCOMMING_MESSAGE_TIMEOUT: float = 1.0


async def process_message(message: Message, command_context: CommandContext) -> None:
    command_cls = getattr(commands, message.type)
    command = command_cls.parse_raw(message.data)
    await command_handler.handle(command, command_context)


class Hanako(App):
    _command_context: CommandContext
    _subscriber: MessageReceiver | None

    def __init__(self, command_context: CommandContext):
        super().__init__()

        self._command_context = command_context
        self._subscriber = None

    def bind(self, subscriber: MessageReceiver) -> None:
        assert not self._subscriber, "Subscriber has been already bound."
        self._subscriber = subscriber

    def build(self) -> uix.RootWidget:
        return uix.RootWidget()

    async def async_run_with(self, *futures: asyncio.Future) -> None:
        await super().async_run("asyncio")

        for future in futures:
            future.cancel()

    async def async_run(self) -> None:
        processor = asyncio.ensure_future(self.process())

        await asyncio.gather(self.async_run_with(processor), processor)

    async def process_once(self) -> None:
        assert self._subscriber, "Subscriber is not bound."
        incomming = self._subscriber.receive(INCOMMING_MESSAGE_TIMEOUT)
        if not incomming:
            return

        await process_message(incomming.unwrap(), self._command_context)
        logger.debug("Processed.")

    async def process(self) -> None:
        try:
            while True:
                await self.process_once()
                await asyncio.sleep(1.0)
        except asyncio.CancelledError:
            logger.info("Canceled.")
