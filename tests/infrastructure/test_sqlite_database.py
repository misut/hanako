import pytest

from hanako.infrastructure import SqliteDatabase


def test_sqlite_database() -> None:
    SqliteDatabase(url="sqlite+aiosqlite:///:memory:?check_same_thread=False")

    with pytest.raises(ValueError):
        SqliteDatabase(url="mysql+pymysql://root:test@localhost:3306")
