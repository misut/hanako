import flet

from hanako.app.routers import endpoint
from hanako.app.settings import initialize_settings


async def desktop_app(page: flet.Page) -> None:
    page.title = "Hanako"
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    await initialize_settings(page)

    async def route_change(e: flet.RouteChangeEvent) -> None:
        if not e.route:
            return

        handler = endpoint.router.get(e.route, None)
        if handler:
            return await handler(page)

        troute = flet.TemplateRoute(e.route)
        for route in endpoint.router.keys():
            if not troute.match(route):
                continue

            handler = endpoint.router[route]
            return await handler(page=page, **troute._TemplateRoute__last_params)

        raise ValueError(f"Unknown Route {e.route}")

    async def view_pop(_: flet.ViewPopEvent) -> None:
        page.views.pop()
        top_view = page.views[-1]
        await page.go_async(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await page.go_async("/")
