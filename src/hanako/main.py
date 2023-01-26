import asyncio

from hanako.interface import app


def run(debug: bool = True) -> None:
    asyncio.run(app.MainApp().async_run(async_lib="asyncio"), debug=debug)
