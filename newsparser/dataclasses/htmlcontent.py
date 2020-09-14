from __future__ import annotations
from enum import Enum
from bs4 import BeautifulSoup
from bs4.element import Tag
from dataclasses import dataclass
from collections import Counter
from typing import Union, Iterator


@dataclass
class HtmlContent:
    content: Union[BeautifulSoup, Tag]

    @classmethod
    def parse(cls, text: str) -> HtmlContent:
        return cls(BeautifulSoup(text))

    @property
    def children(self) -> Iterator[HtmlContent]:
        for x in self.content.children:
            if x.name is not None:
                yield HtmlContent(x)

    @property
    def name(self):
        return self.content.name

    def find_news_contents(self) -> Iterator[TNewsContent]:
        for c in self.children:
            t = c.detect_content_type()
            if t == HtmlContentType.LIST:
                yield ListNewsContent(c.content)
            elif t == HtmlContentType.DICT:
                yield DictNewsContent(c.content)
            else:
                yield from c.find_contents()

    def detect_content_type(self) -> HtmlContentType:
        c = Counter()
        for x in self.children:
            c[x.name] += 1
        # TODO::
        commons = c.most_common(1)
        for _, i in commons:
            if i == 1:
                return HtmlContentType.OTHER
        return HtmlContentType.from_size(len(commons))


class HtmlContentType(Enum):
    LIST = "list"
    DICT = "dict"
    OTHER = "other"

    @classmethod
    def from_size(cls, size: int) -> HtmlContentType:
        if size == 1:
            return cls.LIST
        elif size == 2:
            return cls.DICT
        else:
            return cls.OTHER


@dataclass
class ListNewsContent:
    content: Union[BeautifulSoup, Tag]
    content_type: HtmlContentType = HtmlContentType.LIST


@dataclass
class DictNewsContent:
    content: Union[BeautifulSoup, Tag]
    content_type: HtmlContentType = HtmlContentType.DICT


TNewsContent = Union[ListNewsContent, DictNewsContent]
