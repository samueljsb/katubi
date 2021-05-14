from dataclasses import dataclass
from typing import List, Optional

import requests


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


def lookup_isbn(isbn: str) -> BookInfo:
    """
    Look up a book from its ISBN.

    Raise NotFound if no books could be found with this ISBN.
    """
    # Request data form the Google Books API.
    params = {
        "q": f"isbn:{isbn}",
        "maxResults": "1",  # we only want the top result
    }
    response = requests.get(
        "https://www.googleapis.com/books/v1/volumes", params=params
    )

    # Check we got a response.
    response.raise_for_status()

    # Extract the data and parse it.
    data = response.json()
    if data.get("totalItems", 0) == 0:
        raise NotFound(f"No books found with ISBN {isbn}.")
    return _parse_volume(data["items"][0])


def _parse_volume(data: dict) -> BookInfo:
    return BookInfo(
        title=data["volumeInfo"].get("title", ""),
        subtitle=data["volumeInfo"].get("subtitle", ""),
        authors=data["volumeInfo"].get("authors", []),
        description=data["volumeInfo"].get("description", ""),
        image_url=data["volumeInfo"].get("imageLinks", {}).get("thumbnail"),
    )
