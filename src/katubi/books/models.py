from __future__ import annotations

from typing import Sequence, Tuple

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __repr__(self):
        return f"<Author: {self.name} ({self.pk})>"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=512)
    subtitle = models.CharField(max_length=512, blank=True)

    authors = models.ManyToManyField(Author)

    description = models.TextField(blank=True)

    def __repr__(self):
        return f"<Book: {self.title} ({self.pk})>"

    def __str__(self):
        return self.title

    @classmethod
    def new(
        cls, *, title: str, subtitle: str, authors: Sequence[Author], description: str
    ) -> Book:
        book = cls.objects.create(
            title=title, subtitle=subtitle, description=description
        )
        book.authors.set(authors)
        return book

    @classmethod
    def get_or_create(
        cls,
        *,
        title: str,
        authors: Sequence[Author],
        subtitle: str = "",
        description: str = "",
    ) -> Tuple[Book, bool]:
        """
        Get or create a book with this title and authors.

        Return the book along with a boolean indicating whether a new instance has been
        created.

        If the book does not exist, create it. The subtitle and description are only
        used when creating a new Book instance.
        """
        books = Book.objects.filter(title=title)
        for author in authors:
            books = books.filter(authors=author)

        if not books.exists():
            return (
                cls.new(
                    title=title,
                    subtitle=subtitle,
                    authors=authors,
                    description=description,
                ),
                True,
            )
        # This will throw an error if there is more than one book at this point, but
        # that would be an integrity problem anyway.
        return books.get(), False
