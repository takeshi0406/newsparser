from __future__ import annotations
from enum import Enum
from bs4 import BeautifulSoup
from bs4.element import Tag
from dataclasses import dataclass
from collections import Counter
from typing import Union, Iterator, List, Dict, Tuple


@dataclass
class HtmlContent:
    content: BeautifulSoupHtml

    @classmethod
    def parse(cls, text: str) -> HtmlContent:
        return cls(BeautifulSoup(text).body)

    @property
    def name(self) -> str:
        return self.content.name

    @property
    def children(self) -> Iterator[HtmlContent]:
        for x in self.content.children:
            if x.name is not None:
                yield HtmlContent(x)

    def find_news_contents(self) -> Iterator[TNewsContent]:
        # TODO:: 深さ優先探索にする
        for c in self.children:
            t = c.detect_content_type()
            if t.content_type == HtmlContentType.LIST:
                yield ListNewsContent.convert(c, t)
            elif t.content_type == HtmlContentType.DICT:
                yield DictNewsContent.convert(c, t)
            else:
                yield from c.find_news_contents()

    def detect_content_type(self) -> TContentTypeResult:
        c = Counter(TagEqKey.parse(x.content) for x in self.children)
        commons = c.most_common(1)
        for _, i in commons:
            if i == 1:
                return ContentTypeOtherResult()

        size = len(commons)
        if size == 1:
            return ContentTypeListResult(tag=commons[0][0])
        elif size == 2:
            # TODO:: 順番が保証されてるか確認
            key, value = commons
            return ContentTypeDictResult(key=key[0], value=value[0])
        else:
            return ContentTypeOtherResult()


class HtmlContentType(Enum):
    LIST = "list"
    DICT = "dict"
    OTHER = "other"


@dataclass
class ContentTypeListResult:
    tag: TagEqKey
    content_type: HtmlContentType = HtmlContentType.LIST


@dataclass
class ContentTypeDictResult:
    key: TagEqKey
    value: TagEqKey
    content_type: HtmlContentType = HtmlContentType.DICT


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
                if x.name == result.tag.tag_name
            ],
        )


@dataclass
class DictNewsContent:
    content: BeautifulSoupHtml
    dict_elements: Dict[DictKeyElement, DictValueElement]
    content_type: HtmlContentType = HtmlContentType.DICT

    @classmethod
    def convert(
        cls, content: HtmlContent, result: ContentTypeDictResult
    ) -> DictNewsContent:
        return cls(content=content.content)


@dataclass
class ListElement:
    content: BeautifulSoupHtml

    def title(self) -> str:
        try:
            return self.content.find("title").text
        except Exception:
            print(self.content)
            return None

    def url(self) -> str:
        for k in ["a", "link"]:
            if v := self.content.find(k):
                return v.attrs.get("href", None)
        return None


@dataclass
class DictKeyElement:
    content: BeautifulSoupHtml


@dataclass
class DictValueElement:
    content: BeautifulSoupHtml


@dataclass(eq=True, frozen=True)
class TagEqKey:
    tag_name: str
    tag_id: str
    tag_class: Tuple[str]

    @classmethod
    def parse(cls, content: BeautifulSoupHtml) -> TagEqKey:
        return cls(
            tag_name=content.name,
            tag_id=tuple(content.attrs.get("id", [])),
            tag_class=tuple(content.attrs.get("class", [])),
        )


BeautifulSoupHtml = Union[BeautifulSoup, Tag]
TNewsContent = Union[ListNewsContent, DictNewsContent]
TContentTypeResult = Union[
    ContentTypeListResult, ContentTypeDictResult, ContentTypeOtherResult
]
