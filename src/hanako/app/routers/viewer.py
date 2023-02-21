import flet
from kyrie.models import IDType

from hanako.app.router import Router

router = Router("/viewer")


@router.route("/:manga_id")
async def desktop_viewer(page: flet.Page, manga_id: IDType) -> None:
    view = flet.View(controls=[])

    app_bar = flet.AppBar(
        title=flet.Text(f"Viewer {manga_id}"),
        bgcolor=flet.colors.SURFACE_VARIANT,
    )
    view.controls.append(app_bar)

    lv = flet.ListView(controls=[])
    view.controls.append(lv)

    page.views.append(view)
    await page.update_async()
