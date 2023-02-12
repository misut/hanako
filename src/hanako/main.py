import asyncio

import flet
from kyrie.frameworks import command_bus

from hanako import app
from hanako.command import commands


async def main() -> None:
    await app.initialize_dependencies()
    await flet.app_async(target=app.desktop_app)


def run(debug: bool = True) -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run(debug=False)
