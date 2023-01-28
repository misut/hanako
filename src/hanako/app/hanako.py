import asyncio

from kivy.app import App
from loguru import logger

from hanako.app import widgets
from hanako.drivers import Subscriber
from hanako.interfaces import Message, Receiver

DEFAULT_TIMEOUT: float = 1.0


async def process_once(incomming: Message) -> None:
    print(incomming)


class Hanako(App):
    _subscriber: Receiver

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._subscriber = Subscriber()

    async def process(self, timeout: float = DEFAULT_TIMEOUT) -> None:
        try:
            while True:
                incomming = self._subscriber.receive(timeout)
                if not incomming:
                    # logger.debug("No incomming messages.")
                    await asyncio.sleep(0.1)
                    continue

                await process_once(incomming.unwrap())
                logger.debug("Processed.")
        except asyncio.CancelledError:
            logger.info("Canceled.")

    async def async_run_with(self, *futures: asyncio.Future) -> None:
        await super().async_run("asyncio")

        for future in futures:
            future.cancel()

    async def async_run(self) -> None:
        processor = asyncio.ensure_future(self.process())

        await asyncio.gather(self.async_run_with(processor), processor)

    def build(self) -> widgets.RootWidget:
        return widgets.RootWidget()
