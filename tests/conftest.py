from collections.abc import Iterable

import pytest

SLOW_MARK = "slow"
SLOW_OPTION_KEY = f"--{SLOW_MARK}"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        SLOW_OPTION_KEY,
        action="store_true",
        default=False,
        help=f"Run tests marked as {SLOW_MARK}",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: Iterable[pytest.Item]
) -> None:
    if config.getoption(SLOW_OPTION_KEY):
        return

    skipper = pytest.mark.skip(reason=f"Only run when marked as {SLOW_MARK}")
    for item in items:
        if SLOW_MARK in item.keywords:
            item.add_marker(skipper)
