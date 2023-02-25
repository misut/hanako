from hanako import domain


def test_pool_entry() -> None:
    fetched = domain.PoolEntry.fetch(manga_id="manga_1", language="korean")
    assert isinstance(fetched, domain.PoolEntryFetched)
