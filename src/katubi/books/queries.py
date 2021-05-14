from typing import Tuple

from katubi import lookup

from . import models


def get_or_create_from_isbn(isbn: str) -> Tuple[models.Book, bool]:
    """
    Get or create a Book for the given ISBN. Also get/create the necessary Authors.

    Return the book along with a boolean indicating whether a new record has been
    created.
    """
    info = lookup.lookup_isbn(isbn)
    authors = [
        models.Author.get_or_create(author_name)[0] for author_name in info.authors
    ]
    return models.Book.get_or_create(
        title=info.title,
        subtitle=info.subtitle,
        description=info.description,
        authors=authors,
    )
