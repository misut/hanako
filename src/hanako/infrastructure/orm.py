from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Enum, Integer, String, orm

from hanako.domain import MangaLanguage

BaseOrm = orm.declarative_base()


class MangaOrm(BaseOrm):
    __tablename__ = "manga"

    id: str = Column(String(16), primary_key=True)
    title: str = Column(String(256), index=True, nullable=False)

    cached_in: str = Column(String(256), nullable=True)
    fetched_at: datetime = Column(DateTime, nullable=False)
    updated_at: datetime = Column(DateTime, nullable=False)


class PoolOrm(BaseOrm):
    __tablename__ = "pool"

    id: str = Column(String(36), primary_key=True)
    manga_ids: list[str] = Column(JSON, nullable=False)
    language: MangaLanguage = Column(Enum(MangaLanguage), index=True, nullable=False)
    offset: int = Column(Integer, nullable=False)
    limit: int = Column(Integer, nullable=False)
