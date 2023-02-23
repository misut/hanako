import re
from collections.abc import Callable, Coroutine
from time import time
from typing import Any, cast

import flet
from kyrie.frameworks import command_bus, query_bus
from kyrie.functools import async_partial

from hanako.app.router import Router
from hanako.app.settings import load_settings, save_settings
from hanako.command import commands
from hanako.query import queries, views

router = Router("/settings")


def wrap_with_container(
    control: flet.Control | None = None,
    label: str | None = None,
    on_click: Callable[[flet.ControlEvent], Coroutine[Any, Any, None]] | None = None,
) -> flet.Container:
    row = flet.Row(
        alignment=flet.MainAxisAlignment.CENTER,
        controls=control and [control],
        expand=True,
    )
    if label:
        row.controls.insert(0, flet.Text(value=label, expand=True))

    return flet.Container(
        border_radius=10,
        content=row,
        ink=True,
        on_click=on_click,
        padding=20,
    )


@router.route("/")
async def desktop_settings(page: flet.Page) -> None:
    view = flet.View(controls=[])
    view.appbar = flet.AppBar(
        title=flet.Text("Settings"),
        bgcolor=flet.colors.SURFACE_VARIANT,
    )

    async def change_refresh_on_startup(e: flet.ControlEvent) -> None:
        load_settings(page).refresh_on_startup = e.control.value
        await save_settings(page)

    async def refresh_metadata_only(_: flet.ControlEvent) -> None:
        view = await query_bus().query(
            queries.GetLatestPool(language="all", offset=0, limit=100)
        )
        if view is None:
            return

        pool = cast(views.PoolView, view)
        await command_bus().mdispatch(commands.FetchMangaUsingPool(pool_id=pool.id))

    async def refresh_metadata_and_pool(_: flet.ControlEvent) -> None:
        await command_bus().dispatch(
            commands.FetchPool(language="all", offset=0, limit=100)
        )
        await refresh_metadata_only(_)

    async def click_refresh_pool_manually(_: flet.ControlEvent) -> None:
        column.controls.clear()
        txt_pool_status = flet.Text(size=20)
        column.controls.append(wrap_with_container(control=txt_pool_status))

        view = await query_bus().query(
            queries.GetLatestPool(language="all", ofset=0, limit=100)
        )
        if view is None:
            txt_pool_status.value = "No pool fetched"
        else:
            pool = cast(views.PoolView, view)
            txt_pool_status.value = f"Pool fetched at {pool.fetched_at}"
            column.controls.append(
                wrap_with_container(
                    control=flet.FloatingActionButton(
                        text="Refresh metadata only",
                        width=200,
                        on_click=refresh_metadata_only,
                    )
                )
            )
        column.controls.append(
            wrap_with_container(
                control=flet.FloatingActionButton(
                    bgcolor=flet.colors.SURFACE_VARIANT,
                    text="Refresh metadata and pool",
                    width=200,
                    on_click=refresh_metadata_and_pool,
                )
            )
        )
        await page.update_async()

    def transition_to_general() -> None:
        column.controls.clear()
        swch_refresh_on_startup = flet.Switch(
            value=load_settings(page).refresh_on_startup,
            on_change=change_refresh_on_startup,
        )
        column.controls.append(
            wrap_with_container(
                control=swch_refresh_on_startup, label="Refresh pool on startup"
            )
        )

        column.controls.append(
            wrap_with_container(
                label="Refresh metadata and pool manually",
                on_click=click_refresh_pool_manually,
            )
        )

    async def change_theme_mode(e: flet.ControlEvent) -> None:
        theme_mode = flet.ThemeMode(e.control.value)
        load_settings(page).theme_mode = theme_mode
        await save_settings(page)

        page.theme_mode = theme_mode
        await page.update_async()

    def transition_to_theme() -> None:
        column.controls.clear()
        drop_theme_mode = flet.Dropdown(
            options=[
                flet.dropdown.Option(key="light", text="Light"),
                flet.dropdown.Option(key="dark", text="Dark"),
                flet.dropdown.Option(key="system", text="System"),
            ],
            value=load_settings(page).theme_mode.value,
            on_change=change_theme_mode,
        )
        column.controls.append(
            wrap_with_container(drop_theme_mode, "Select theme mode")
        )

    devs: list[float] = []

    async def btn_rail(event: flet.ControlEvent) -> None:
        dev = time()
        if len(devs) == 0 or dev - devs[-1] < 0.2:
            devs.append(dev)
        else:
            devs.clear()
        if len(devs) >= 5:
            devs.clear()
            return await page.go_async("/settings/developer")

        match event.control.selected_index:
            case 0:
                transition_to_general()
                await page.update_async()

            case 1:
                transition_to_theme()
                await page.update_async()

            case _:
                devs.clear()
                rail.selected_index = None
                await page.go_async("/settings/developer")

    rail = flet.NavigationRail(
        selected_index=0,
        label_type=flet.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        # leading=flet.FloatingActionButton(icon=flet.icons.FAVORITE),
        group_alignment=-0.9,
        destinations=[
            flet.NavigationRailDestination(
                icon=flet.icons.SETTINGS_OUTLINED,
                selected_icon=flet.icons.SETTINGS,
                label="General",
            ),
            flet.NavigationRailDestination(
                icon=flet.icons.BRUSH_OUTLINED,
                selected_icon=flet.icons.BRUSH,
                label="Theme",
            ),
        ],
        on_change=btn_rail,
    )
    if load_settings(page).developer_mode:
        rail.destinations.append(
            flet.NavigationDestination(
                icon=flet.icons.DEVELOPER_MODE_OUTLINED,
                selected_icon=flet.icons.DEVELOPER_MODE,
                label="Developer",
            )
        )

    column = flet.Column(
        controls=[],
        alignment=flet.MainAxisAlignment.START,
        horizontal_alignment=flet.CrossAxisAlignment.END,
        expand=True,
    )
    transition_to_general()

    row = flet.Row(
        controls=[rail, flet.VerticalDivider(width=1), column],
        alignment=flet.MainAxisAlignment.START,
        height=page.height - 76,
    )
    view.controls.append(row)

    page.views.append(view)
    await page.update_async()


@router.route("/developer")
async def desktop_developer_settings(page: flet.Page) -> None:
    view = flet.View(controls=[])
    view.appbar = flet.AppBar(
        title=flet.Text("Developer Settings"),
        bgcolor=flet.colors.SURFACE_VARIANT,
    )

    column = flet.Column()
    view.controls.append(column)

    async def change_developer_mode(e: flet.ControlEvent) -> None:
        load_settings(page).developer_mode = e.control.value
        await save_settings(page)

        developer_mode = load_settings(page).developer_mode
        txt_search.disabled = not developer_mode
        await page.update_async()

    swch_developer_mode = flet.Switch(
        value=load_settings(page).developer_mode,
        on_change=change_developer_mode,
    )
    column.controls.append(
        wrap_with_container(control=swch_developer_mode, label="Turn On Developer Mode")
    )

    container = wrap_with_container()

    async def click_manga(manga_id: str, _: flet.ControlEvent) -> None:
        await command_bus().dispatch(commands.CacheManga(manga_id=manga_id))

    async def txt_submit(e: flet.ControlEvent) -> None:
        nonlocal container
        row: flet.Row = container.content
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
                    on_click=async_partial(click_manga, manga_view.id),
                )
            )

        await page.update_async()

    txt_search = flet.TextField(
        disabled=not load_settings(page).developer_mode,
        hint_text="Please enter manga id here",
        keyboard_type=flet.KeyboardType.NUMBER,
        label="Search Manga",
        on_submit=txt_submit,
        prefix_icon=flet.icons.SEARCH,
        width=400,
    )
    column.controls.append(wrap_with_container(control=txt_search))
    column.controls.append(container)

    page.views.append(view)
    await page.update_async()
