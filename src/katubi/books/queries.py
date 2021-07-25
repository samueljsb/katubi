from typing import Sequence

from . import models


def get_or_create_author(name: str) -> tuple[models.Author, bool]:
    """
    Retrieve or create an Author record.
    """
    return models.Author.objects.get_or_create(name=name)


def get_or_create_book(
    *,
    title: str,
    authors: Sequence[models.Author],
    subtitle: str = "",
    description: str = "",
) -> tuple[models.Book, bool]:
    """
    Get or create a book with this title and authors.

    Return the book along with a boolean indicating whether a new instance has been
    created.

    If the book does not exist, create it. The subtitle and description are only
    used when creating a new Book instance.
    """
    books = models.Book.objects.filter(title=title)
    for author in authors:
        books = books.filter(authors=author)

    try:
        return books.get(), False
    except models.Book.DoesNotExist:
        return (
            _new_book(
                title=title,
                subtitle=subtitle,
                authors=authors,
                description=description,
            ),
            True,
        )


def _new_book(
    *,
    title: str,
    subtitle: str,
    authors: Sequence[models.Author],
    description: str,
) -> models.Book:
    """
    Record a new record of a book.
    """
    book = models.Book.objects.create(
        title=title, subtitle=subtitle, description=description
    )
    book.authors.set(authors)
    return book
