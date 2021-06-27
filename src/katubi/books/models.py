from __future__ import annotations

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
