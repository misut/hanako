from collections.abc import Callable

import sqlalchemy
from sqlalchemy import orm as sqlalchemyorm

from hanako.drivers.orm import BaseOrm


class SqlDatabase:
    _engine: sqlalchemy.Engine
    _session_factory: Callable[..., sqlalchemyorm.Session]

    def __init__(self, url: str) -> None:
        self._engine = sqlalchemy.create_engine(url=url)
        self._session_factory = sqlalchemyorm.sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    def create_all(self) -> None:
        BaseOrm.metadata.create_all(self._engine)

    def drop_all(self) -> None:
        BaseOrm.metadata.drop_all(self._engine)

    def session(self) -> sqlalchemyorm.Session:
        return self._session_factory()
