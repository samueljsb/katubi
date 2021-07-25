from typing import Optional, Tuple

import isbnlib

from katubi import lookup as google_books
from katubi.books import models as book_models
from katubi.books import queries as book_queries
from katubi.volumes import models, operations


def get_or_create_volume_for_isbn(isbn: str) -> Tuple[models.Volume, bool]:
    """
    Retrieve the volume with this ISBN.

    If the volume does not exist in our records, look up its information and record it.

    Returns the volume along with a boolean indicating whether a new instance has been
    created.

    Raises NotFound if there is no volume recorded for this ISBN and no information
    could be found from Google Books.
    """
    # Return an existing volume if one exists.
    volume = _get_volume_for_isbn(isbn)
    if volume is not None:
        return volume, False

    # Create a new volume.
    volume_info = google_books.lookup_isbn(isbn)
    book = _get_or_create_book(volume_info)
    return (
        operations.new_volume(
            book=book, isbn=isbn, cover_image_url=volume_info.image_url
        ),
        True,
    )


def _get_volume_for_isbn(isbn: str) -> Optional[models.Volume]:
    """
    Retrieve the volume with the given ISBN.

    If no volume is found with the given ISBN, return None.
    """
    # Clean the ISBN.
    isbn = isbnlib.ean13(isbn)

    try:
        return models.Volume.objects.get(isbn=isbn)
    except models.Volume.DoesNotExist:
        return None


def _get_or_create_book(info: google_books.VolumeInfo) -> book_models.Book:
    """
    Retrieve (or create) the book for given volume information.
    """
    authors = []
    for author_name in info.authors:
        author, __ = book_queries.get_or_create_author(author_name)
        authors.append(author)

    book, __ = book_queries.get_or_create_book(
        title=info.title,
        authors=authors,
        subtitle=info.subtitle,
        description=info.description,
    )
    return book
