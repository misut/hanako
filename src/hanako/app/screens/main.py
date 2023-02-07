from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView

from hanako.app.uix.behaviors import QueryBehavior


class MainScreen(Screen):
    ...


class MangaListView(RecycleView):
    ...


class SearchView(QueryBehavior, ScrollView):
    ...


class AppbarView(ScrollView):
    ...


class SidebarView(ScrollView):
    ...
