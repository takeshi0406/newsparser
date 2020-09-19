from __future__ import annotations
from enum import Enum
from bs4 import BeautifulSoup
from bs4.element import Tag
from dataclasses import dataclass
from collections import Counter
from typing import Union, Iterator, List, Tuple

IGNORE_TAGS = {"script", "meta"}


@dataclass
class HtmlContent:
    content: BeautifulSoupHtml

    @classmethod
    def parse(cls, text: str) -> HtmlContent:
        return cls(BeautifulSoup(text, "html5lib"))

    @property
    def name(self) -> str:
        return self.content.name

    @property
    def children(self) -> Iterator[HtmlContent]:
        for x in self.content.children:
            if x.name is not None and x.name not in IGNORE_TAGS:
                yield HtmlContent(x)

    @property
    def tag_key(self) -> TagEqKey:
        return TagEqKey.parse(self.content)

    def find_news_contents(self) -> Iterator[TNewsContent]:
        for c in self.children:
            t = c.detect_content_type()
            if t.content_type == HtmlContentType.LIST:
                yield ListNewsContent.convert(c, t)
            yield from c.find_news_contents()

    def detect_content_type(self) -> TContentTypeResult:
        c = Counter(TagEqKey.parse(x.content) for x in self.children)
        commons = c.most_common(2)
        if (
            # one type and multiple tags exist
            (len(commons) == 1 and commons[0][1] != 1)
            # Multiple type and one top tag exists
            or (len(commons) == 2 and len(set(c for _, c in commons)) == 2)
        ):
            return ContentTypeListResult(tag_key=commons[0][0])
        else:
            return ContentTypeOtherResult()


class HtmlContentType(Enum):
    LIST = "list"
    OTHER = "other"


@dataclass
class ContentTypeListResult:
    tag_key: TagEqKey
    content_type: HtmlContentType = HtmlContentType.LIST


@dataclass
class ContentTypeOtherResult:
    content_type: HtmlContentType = HtmlContentType.OTHER


@dataclass
class ListNewsContent:
    content: BeautifulSoupHtml
    list_elements: List[ListElement]
    content_type: HtmlContentType = HtmlContentType.LIST

    @classmethod
    def convert(
        cls, content: HtmlContent, result: ContentTypeListResult
    ) -> ListNewsContent:
        return cls(
            content=content.content,
            list_elements=[
                ListElement(x.content)
                for x in content.children
                if x.tag_key == result.tag_key
            ],
        )


@dataclass
class ListElement:
    content: BeautifulSoupHtml

    def title(self) -> str:
        titles = self.content.find_all("title") + self.content.find_all(
            class_=lambda x: x and "title" in x
        )
        for x in titles:
            return x.text.strip()

        for k in ["h1", "h2", "h3", "h4", "p", "a"]:
            if vs := self.content.find_all(k):
                # TODO:: maxが違いそうなので、一度xpathに変換
                v = max(vs, key=lambda x: len(x.text.strip()))
                return v.text.strip()

        return None

    def url(self) -> str:
        for k in ["a", "link"]:
            if v := self.content.find(k):
                return v.attrs.get("href", None)
        return None


@dataclass(eq=True, frozen=True)
class TagEqKey:
    tag_name: str
    tag_id: Tuple[str]
    tag_class: Tuple[str]

    @classmethod
    def parse(cls, content: BeautifulSoupHtml) -> TagEqKey:
        return cls(
            tag_name=content.name,
            tag_id=tuple(content.attrs.get("id", [])),
            tag_class=tuple(content.attrs.get("class", [])),
        )


BeautifulSoupHtml = Union[BeautifulSoup, Tag]
TNewsContent = Union[ListNewsContent]
TContentTypeResult = Union[ContentTypeListResult, ContentTypeOtherResult]
