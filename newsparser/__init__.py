from typing import List
from newsparser.dataclasses import NewsContent
from newsparser.dataclasses.htmlcontent import HtmlContent


class NewsParser:
    def __init__(self):
        pass

    def parse(self, text: str) -> List[NewsContent]:
        html = HtmlContent.parse(text)
        for x in html.find_news_contents():
            for y in x.list_elements:
                print(y.title())
                print(y.url())
            print("--" * 100)
        return [NewsContent(title="", url="url")]
