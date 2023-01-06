import asyncio

from kivy.app import App

from hanako import widgets


class MainApp(App):
    def build(self) -> widgets.MainWidget:
        return widgets.MainWidget()


def run() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(MainApp().async_run(async_lib="asyncio"))
    loop.close()
