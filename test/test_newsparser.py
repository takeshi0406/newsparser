import pytest
import requests
from newsparser import NewsParser


@pytest.mark.parametrize(
    "url", ["https://kiito.hatenablog.com/feed", "https://akihata.jp/news/"]
)
def test(url):
    res = requests.get(url)
    res.raise_for_status()
    NewsParser().parse(res.text)
