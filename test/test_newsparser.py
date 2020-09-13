import requests
from newsparser import NewsParser


def test():
    res = requests.get("https://kiito.hatenablog.com/feed")
    res.raise_for_status()
    NewsParser().parse(res.text)
