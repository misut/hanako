import flet
import pydantic

DEFAULT_HANAKO_SETTINGS_KEY = "hanako.settings"


class Settings(pydantic.BaseSettings):
    refresh_on_startup: bool = False
    theme_mode: flet.ThemeMode = flet.ThemeMode.SYSTEM


async def initialize_settings(page: flet.Page) -> None:
    settings_json = await page.client_storage.get_async(DEFAULT_HANAKO_SETTINGS_KEY)
    try:
        settings = Settings.parse_raw(settings_json)
    except pydantic.ValidationError:
        settings = Settings()
        await page.client_storage.set_async(
            DEFAULT_HANAKO_SETTINGS_KEY, settings.json()
        )

    page.theme_mode = settings.theme_mode
    page.settings = settings


def load_settings(page: flet.Page) -> Settings:
    return page.settings


async def save_settings(page: flet.Page) -> None:
    await page.client_storage.set_async(
        DEFAULT_HANAKO_SETTINGS_KEY, load_settings(page).json()
    )
