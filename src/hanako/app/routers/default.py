from typing import cast

import flet
from kyrie.frameworks import command_bus, query_bus
from kyrie.functools import P, async_partial
from kyrie.models import IDType

from hanako.app.router import Router
from hanako.command import commands
from hanako.query import queries, views

router = Router()


async def translate_to_viewer(manga_id: IDType, _: flet.ControlEvent) -> None:
    await _.page.go_async(f"/viewer/{manga_id}/")


def manga_container(
    manga: views.MangaView, thumbnail_width: int = 100
) -> flet.Container:
    return flet.Container(
        border_radius=10,
        content=flet.Row(
            controls=[
                flet.Stack(
                    controls=[
                        flet.Image(
                            border_radius=flet.border_radius.only(10, 0, 10, 0),
                            src_base64=manga.thumbnail,
                            width=thumbnail_width,
                        ),
                        flet.Container(
                            alignment=flet.alignment.center,
                            blend_mode=flet.BlendMode.SRC_OVER,
                            border_radius=flet.border_radius.only(10, 0, 10, 0),
                            content=flet.Image(
                                opacity=0,
                                src_base64=manga.thumbnail,
                                width=thumbnail_width,
                            ),
                            gradient=flet.LinearGradient(
                                begin=flet.alignment.top_center,
                                end=flet.alignment.bottom_center,
                                colors=[flet.colors.TRANSPARENT, flet.colors.BLACK87],
                            ),
                        ),
                        flet.Text(
                            bottom=3,
                            color=flet.colors.WHITE70,
                            right=3,
                            value=f"{manga.id} | p{manga.num_pages}",
                            size=10,
                        ),
                    ],
                ),
                flet.Column(
                    controls=[
                        flet.Text(
                            style=flet.TextThemeStyle.LABEL_LARGE,
                            value=manga.title.strip(" "),
                        ),
                        flet.Text(
                            style=flet.TextThemeStyle.LABEL_SMALL,
                            value="",
                        ),
                    ],
                ),
            ],
            spacing=20,
        ),
        ink=True,
        on_click=async_partial(translate_to_viewer, manga.id),
    )


@router.route("/")
async def desktop_main(page: flet.Page) -> None:
    view = flet.View(controls=[])
    view.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    view.vertical_alignment = flet.MainAxisAlignment.START
    view.padding = flet.padding.symmetric(20, 40)

    async def go_settings(_: flet.ControlEvent) -> None:
        await page.go_async("/settings/")

    btn_go_settings = flet.FloatingActionButton(
        icon=flet.icons.SETTINGS_OUTLINED,
        on_click=go_settings,
        shape=flet.CircleBorder(),
    )
    view.floating_action_button = btn_go_settings

    column = flet.Column(controls=[], expand=True)
    view.controls.append(column)

    txt_title = flet.Text(
        style=flet.TextThemeStyle.HEADLINE_SMALL, value="Recently Added"
    )
    column.controls.append(txt_title)
    column.controls.append(flet.Divider())

    lv = flet.ListView(controls=[], expand=True, spacing=10)
    column.controls.append(lv)

    page.views.append(view)
    await page.update_async()

    pool_id = await command_bus().dispatch(
        commands.FetchPool(language="korean", offset=0, limit=10)
    )
    await command_bus().mdispatch(commands.FetchMangaUsingPool(pool_id=pool_id))

    found = await query_bus().query(queries.GetPool(pool_id=pool_id))
    assert found
    pool = cast(views.PoolView, found)

    mangas: list[views.MangaView] = []
    for manga_id in pool.id_list:
        manga = await query_bus().query(queries.GetManga(manga_id=manga_id))
        if manga is None:
            continue

        manga = cast(views.MangaView, manga)
        mangas.append(manga)

    for manga in mangas:
        lv.controls.append(manga_container(manga))

    await page.update_async()
