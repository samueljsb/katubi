from typing import Optional

import isbnlib

from katubi.books import models as book_models

from . import models


def new_volume(
    *, book: book_models.Book, isbn: Optional[str], cover_image_url: Optional[str]
) -> models.Volume:
    """
    Record a new volume.
    """
    # Clean the ISBN.
    if isbn:
        isbn = isbnlib.ean13(isbn)

    return models.Volume.objects.create(
        book=book, isbn=isbn, cover_image_url=cover_image_url or ""
    )
