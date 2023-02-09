from typing import List
from dataclasses import dataclass


@dataclass
class PageLink:
    title: str
    href: str | None = None


@dataclass
class Breadcrumb:
    title: str
    links: List[PageLink]
    href: str | None = None
