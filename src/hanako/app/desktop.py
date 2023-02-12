import re
from typing import cast

import flet
from kyrie.frameworks import query_bus

from hanako.query import queries, views


async def desktop_app(page: flet.Page) -> None:
    page.title = "Hanako"
    page.vertical_alignment = flet.MainAxisAlignment.CENTER

    row = flet.Row([], alignment=flet.MainAxisAlignment.CENTER)

    async def txt_submit(e: flet.ControlEvent) -> None:
        nonlocal row
        row.controls.clear()

        manga_id: str = e.control.value
        if re.fullmatch(r"[0-9]+", manga_id) is None:
            row.controls.append(flet.Text(f"Invalid Manga ID - {manga_id}"))
            return await page.update_async()

        manga_view = await query_bus().query(queries.GetManga(manga_id=manga_id))
        if manga_view is None:
            row.controls.append(flet.Text(f"No Manga Searched By ID - {manga_id}"))
        else:
            manga_view = cast(views.MangaView, manga_view)
            row.controls.append(
                flet.Container(
                    content=flet.Row(
                        [
                            flet.Image(
                                src_base64=manga_view.thumbnail,
                                width=100,
                                height=100,
                                fit=flet.ImageFit.FIT_HEIGHT,
                                repeat=flet.ImageRepeat.NO_REPEAT,
                            ),
                            flet.Text(manga_view.title),
                        ]
                    ),
                    ink=True,
                    on_click=lambda _: print("Hello, world"),
                )
            )

        await page.update_async()

    txt_search = flet.TextField(
        autofocus=True,
        hint_text="Please enter hitomi gallery id here",
        keyboard_type=flet.KeyboardType.NUMBER,
        label="Search",
        on_submit=txt_submit,
        prefix_icon=flet.icons.SEARCH,
        width=400,
    )

    await page.add_async(
        flet.Row(
            [txt_search],
            alignment=flet.MainAxisAlignment.CENTER,
        ),
        row,
    )
