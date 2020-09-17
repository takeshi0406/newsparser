import pytest
import requests
from newsparser import NewsParser


@pytest.mark.parametrize(
    "url",
    [
        # "https://kiito.hatenablog.com/feed",
        # "https://akihata.jp/news/",
        # "https://avex.jp/pripara/news/",
        # "https://www.suruga-ya.jp/search?category=&search_word=%E9%9B%BB%E6%B3%A2%E3%82%BD%E3%83%B3%E3%82%B0&searchbox=1&is_marketplace=0",
        # "http://t7s.jp/news/category_all/",
        # "https://dempagumi.tokyo/news/",
        # "https://cametek.jp/",
        # "https://chiebukuro.yahoo.co.jp/search/?p=%E9%9B%BB%E6%B3%A2%E3%82%BD%E3%83%B3%E3%82%B0&aq=-1&ei=UTF-8&class=1&fr=pc_det_resrch",
        "https://natalie.mu/music/news/list/artist_id/5606"
    ],
)
def test(url):
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    res.raise_for_status()
    NewsParser().parse(res.text)
