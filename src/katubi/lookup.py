from dataclasses import dataclass
from typing import List, Optional


class NotFound(Exception):
    """
    No books found for the given search terms.
    """


@dataclass(frozen=True)
class BookInfo:
    title: str
    subtitle: str
    authors: List[str]
    description: str
    image_url: Optional[str]


def lookup_isbn(isbn: str):
    """
    Look up a book from its ISBN.

    Raise NotFound if no books could be found with this ISBN.
    """
    raise NotImplementedError
