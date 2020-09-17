import pytest
import requests
from newsparser import NewsParser


@pytest.mark.parametrize(
    "url",
    [
        # "https://kiito.hatenablog.com/feed",
        # "https://akihata.jp/news/",
        # "https://avex.jp/pripara/news/",
        "https://www.suruga-ya.jp/search?category=&search_word=%E9%9B%BB%E6%B3%A2%E3%82%BD%E3%83%B3%E3%82%B0&searchbox=1&is_marketplace=0",
    ],
)
def test(url):
    res = requests.get(url)
    res.raise_for_status()
    NewsParser().parse(res.text)
