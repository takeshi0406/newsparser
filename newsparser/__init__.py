from typing import List
from newsparser.dataclasses import NewsContent
from newsparser.dataclasses.htmlcontent import HtmlContent


class NewsParser:
    def __init__(self):
        pass

    def parse(self, text: str) -> List[NewsContent]:
        html = HtmlContent.parse(text)
        result = []
        for x in html.find_news_contents():
            for y in x.list_elements:
                if all(z is not None for z in (y.title(), y.url())):
                    result.append(NewsContent(title=y.title(), url=y.url()))
        return result
