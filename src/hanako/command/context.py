from collections.abc import Callable

from hanako.drivers import Hitomi
from hanako.models import Context


class CommandContext(Context):
    hitomi: Callable[[], Hitomi]
