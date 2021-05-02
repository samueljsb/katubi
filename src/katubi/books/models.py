from __future__ import annotations

from typing import List

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)

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
        cls, *, title: str, subtitle: str, authors: List[str], description: str
    ) -> Book:
        book = cls.objects.create(
            title=title, subtitle=subtitle, description=description
        )

        for author_name in authors:
            author, _created = Author.objects.get_or_create(name=author_name)
            book.authors.add(author)

        return book
