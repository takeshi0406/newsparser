from typing import List
from newsparser.dataclasses import NewsContent
from newsparser.dataclasses.htmlcontent import HtmlContent


class NewsParser:
    def __init__(self):
        pass

    def parse(self, text: str) -> List[NewsContent]:
        html = HtmlContent.parse(text)
        for x in html.find_news_contents():
            print("found")
        return [NewsContent(title="", url="url")]
