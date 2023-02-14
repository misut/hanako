import flet

from hanako.app.router import Router
from hanako.app.settings import load_settings, save_settings

router = Router("/settings")


@router.route("/")
async def desktop_settings(page: flet.Page) -> None:
    app_bar = flet.AppBar(
        title=flet.Text("Settings"),
        bgcolor=flet.colors.SURFACE_VARIANT,
    )

    async def change_refresh_on_startup(e: flet.ControlEvent) -> None:
        load_settings(page).refresh_on_startup = e.control.value
        await save_settings(page)

    def transition_to_general() -> None:
        column.controls.clear()
        swch_refresh_on_startup = flet.Switch(
            label="Refresh on startup",
            value=load_settings(page).refresh_on_startup,
            on_change=change_refresh_on_startup,
        )
        column.controls.append(swch_refresh_on_startup)

    async def change_theme_mode(e: flet.ControlEvent) -> None:
        theme_mode = flet.ThemeMode(e.control.value)
        load_settings(page).theme_mode = theme_mode
        await save_settings(page)

        page.theme_mode = theme_mode
        await page.update_async()

    def transition_to_theme() -> None:
        column.controls.clear()
        drop_theme_mode = flet.Dropdown(
            label="Select mode",
            options=[
                flet.dropdown.Option(key="light", text="Light"),
                flet.dropdown.Option(key="dark", text="Dark"),
                flet.dropdown.Option(key="system", text="System"),
            ],
            value=load_settings(page).theme_mode.value,
            on_change=change_theme_mode,
        )
        column.controls.append(drop_theme_mode)

    async def btn_rail(event: flet.ControlEvent) -> None:
        match event.control.selected_index:
            case 0:
                transition_to_general()
                await page.update_async()

            case 1:
                transition_to_theme()
                await page.update_async()

    rail = flet.NavigationRail(
        selected_index=0,
        label_type=flet.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        height=page.height,
        leading=flet.FloatingActionButton(icon=flet.icons.FAVORITE),
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

    column = flet.Column(
        controls=[],
        alignment=flet.MainAxisAlignment.START,
        expand=True,
    )
    transition_to_general()

    row = flet.Row(controls=[rail, flet.VerticalDivider(width=1), column])

    view = flet.View(controls=[app_bar, row])
    page.views.append(view)
    await page.update_async()
