from typing import cast
import flet

from kyrie.frameworks import query_bus
from kyrie.functools import async_partial
from kyrie.models import IDType

from hanako.app.router import Router
from hanako.query import queries, views

router = Router()


async def translate_to_viewer(manga_id: IDType, _: flet.ControlEvent) -> None:
    print(manga_id)
    await _.page.go_async(f"/viewer/{manga_id}/")


def manga_container(manga: views.MangaView) -> flet.Container:
    return flet.Container(
        content=flet.Row(
            [
                flet.Image(src_base64=manga.thumbnail, width=140),
                flet.Column(
                    controls=[flet.Text(value=manga.title), flet.Text(value=manga.id)]
                ),
            ]
        ),
        ink=True,
        on_click=async_partial(translate_to_viewer, manga.id),
    )


@router.route("/")
async def desktop_main(page: flet.Page) -> None:
    view = flet.View(controls=[])

    async def go_settings(_: flet.ControlEvent) -> None:
        await page.go_async("/settings/")

    btn_go_settings = flet.FloatingActionButton(
        icon=flet.icons.SETTINGS_OUTLINED,
        on_click=go_settings,
        shape=flet.CircleBorder(),
    )
    view.floating_action_button = btn_go_settings

    lv = flet.ListView(controls=[], expand=True, spacing=10)
    view.controls.append(lv)

    manga_ids = ["2466885", "2466883", "2466879", "2466877", "2466876"]
    mangas: list[views.MangaView] = []
    for manga_id in manga_ids:
        manga = await query_bus().query(queries.GetManga(manga_id=manga_id))
        if manga is None:
            continue

        manga = cast(views.MangaView, manga)
        mangas.append(manga)

    for manga in mangas:
        lv.controls.append(manga_container(manga))

    page.views.append(view)
    await page.update_async()
