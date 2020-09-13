from typing import List
from newsparser.dataclasses import NewsContent


class NewsParser:
    def __init__(self):
        pass

    def parse(self, text: str) -> List[NewsContent]:
        return [NewsContent(title="", url="url")]
