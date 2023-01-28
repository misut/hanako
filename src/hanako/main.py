import asyncio

from hanako import app


def run(debug: bool = True) -> None:
    asyncio.run(app.Hanako().async_run(), debug=debug)
