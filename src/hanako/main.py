import asyncio

import aiosqlite
import flet

from hanako import app


async def main() -> None:
    await app.initialize_dependencies()
    await flet.app_async(target=app.desktop_app)


def run(debug: bool = True) -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run(debug=False)
