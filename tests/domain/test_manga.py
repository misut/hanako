import pytest

from hanako import domain


def test_manga() -> None:
    fetched = domain.Manga.fetch(
        id="manga_1",
        language="korean",
        title="test_manga",
        thumbnail="",
        artists=[],
        pages=[
            domain.MangaPage(
                filename="test_page_1", hash="", hasavif=False, haswebp=False
            )
        ],
        tags=[],
    )
    assert isinstance(fetched, domain.MangaFetched)

    manga = fetched.entity
    with pytest.raises(domain.PageNumberError):
        manga.cache_page(-1, "")
    with pytest.raises(domain.PageNumberError):
        manga.cache_page(1, "")
    with pytest.raises(domain.PageCachedPathError):
        manga.cache_page(0, "src")

    page_cached = manga.cache_page(0, "pyproject.toml")
    assert isinstance(page_cached, domain.MangaPageCached)
