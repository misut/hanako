from typing import cast

import flet
from kyrie.frameworks import command_bus, query_bus
from kyrie.models import IDType

from hanako.app.router import Router
from hanako.command import commands
from hanako.query import queries, views

router = Router("/viewer")


@router.route("/:manga_id")
async def desktop_viewer(page: flet.Page, manga_id: IDType) -> None:
    view = flet.View(controls=[])
    view.appbar = flet.AppBar(
        title=flet.Text(f"Viewer {manga_id}"),
        bgcolor=flet.colors.SURFACE_VARIANT,
    )
    view.horizontal_alignment = flet.CrossAxisAlignment.CENTER

    lv = flet.ListView(controls=[], width=600)
    view.controls.append(lv)

    page.views.append(view)
    page.splash = flet.ProgressRing()
    await page.update_async()

    await command_bus().mdispatch(commands.CacheManga(manga_id=manga_id))
    manga = await query_bus().query(queries.GetManga(manga_id=manga_id))
    assert manga is not None
    manga = cast(views.MangaView, manga)

    for manga_page in manga.pages:
        lv.controls.append(
            flet.Image(src=manga_page.cached_in, fit=flet.ImageFit.FIT_HEIGHT)
        )

    view.scroll = flet.ScrollMode.ALWAYS
    page.splash = None
    await page.update_async()
