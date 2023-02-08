from dataclasses import dataclass

from kyrie.context import Context


@dataclass(frozen=True)
class QueryContext(Context):
    ...
