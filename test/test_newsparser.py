import pytest
from pathlib import Path
from newsparser import NewsParser


@pytest.fixture
def htmls():
    result = {}
    for p in Path("test/data/htmls").iterdir():
        with p.open("r") as f:
            result[p.name] = f.read()
    return result


def test(htmls):
    for key, html in htmls.items():
        NewsParser().parse(html)
