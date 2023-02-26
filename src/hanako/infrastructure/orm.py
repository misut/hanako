import abc
from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from hanako.domain import MangaLanguage


class BaseOrm(DeclarativeBase):
    pass


class MangaOrm(BaseOrm):
    __tablename__ = "manga"

    id: Mapped[str] = mapped_column(String(16), primary_key=True)
    language: Mapped[MangaLanguage] = mapped_column(
        Enum(MangaLanguage), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(256), index=True, nullable=False)
    thumbnail: Mapped[str] = mapped_column(Text, nullable=False)
    artists: Mapped[list[dict[str, bool | str | None]]] = mapped_column(
        JSON, nullable=False
    )
    pages: Mapped[list[dict[str, bool | str | None]]] = mapped_column(
        JSON, nullable=False
    )
    tags: Mapped[list[dict[str, bool | str | None]]] = mapped_column(
        JSON, nullable=False
    )

    fetched_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class PoolEntryOrm(BaseOrm):
    __tablename__ = "pool_entry"

    manga_id: Mapped[str] = mapped_column(String(16), primary_key=True)
    language: Mapped[MangaLanguage] = mapped_column(
        Enum(MangaLanguage), index=True, nullable=False
    )

    fetched_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
