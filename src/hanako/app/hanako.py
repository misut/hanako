import asyncio
import pathlib

from kivy.app import App, Builder
from kivy.factory import Factory
from loguru import logger

from hanako.app import root_widget
from hanako.command import CommandContext, command_context, command_handler, commands
from hanako.interfaces import Message, MessageReceiver

DEFAULT_KV_ROOT: str = "src/hanako/app"
INCOMMING_MESSAGE_TIMEOUT: float = 1.0


def build_kv_files(root: str | pathlib.Path) -> None:
    kv_root = pathlib.Path(root)
    kv_files: list[str] = []
    for kv_file in kv_root.iterdir():
        if kv_file.is_dir():
            build_kv_files(kv_file)
        if kv_file.suffix != ".kv":
            continue
        if kv_file.absolute() == pathlib.Path(__file__).with_suffix(".kv"):
            continue
        kv_files.append(str(kv_file))
        logger.debug(f"Loading {kv_file.absolute()}")

    for f in kv_files:
        Builder.load_file(f)
        logger.debug(f"Loaded {f}")


def register_factories() -> None:
    register = Factory.register
    register("RootWidget", module="hanako.app.root_widget")

    register("CommandBehavior", module="hanako.app.uix.behaviors")
    register("HoverBehavior", module="hanako.app.uix.behaviors")
    register("QueryBehavior", module="hanako.app.uix.behaviors")
    register("ImageButton", module="hanako.app.uix.image_button")
    register("MangaDetail", module="hanako.app.uix.manga_detail")

    register("MainScreen", module="hanako.app.screens.main")


async def process_message(message: Message, command_context: CommandContext) -> None:
    command_cls = getattr(commands, message.type)
    command = command_cls.parse_raw(message.data)
    await command_handler.handle(command, command_context)


class Hanako(App):
    _subscriber: MessageReceiver | None

    def __init__(self):
        super().__init__()

        self._subscriber = None

    def bind(self, subscriber: MessageReceiver) -> None:
        assert not self._subscriber, "Subscriber has been already bound."
        self._subscriber = subscriber

    def build(self) -> root_widget.RootWidget:
        build_kv_files(DEFAULT_KV_ROOT)
        register_factories()
        return root_widget.RootWidget()

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

        await process_message(incomming.unwrap(), command_context())
        logger.debug("Processed.")

    async def process(self) -> None:
        try:
            while True:
                await self.process_once()
                await asyncio.sleep(1.0)
        except asyncio.CancelledError:
            logger.info("Canceled.")
