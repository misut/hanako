import flet

from hanako.app.routers import endpoint
from hanako.app.settings import initialize_settings, load_settings


async def desktop_app(page: flet.Page) -> None:
    await initialize_settings(page)

    async def route_change(e: flet.RouteChangeEvent) -> None:
        handler = endpoint.router.get(e.route, None)
        if not handler:
            return

        await handler(page)

    async def view_pop(e: flet.ViewPopEvent) -> None:
        page.views.pop()
        top_view = page.views[-1]
        await page.go_async(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await page.go_async("/")
    await page.go_async("/settings/")
