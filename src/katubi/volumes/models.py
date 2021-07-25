from django.db import models
from django.db.models import Q, UniqueConstraint

from katubi.books import models as book_models


class Volume(models.Model):
    """
    A volume record represents a specific publication of a given book, uniquely identified by ISBN.

    Note that this does not represent a single physical object: two identical codices
    would be represented by a single volume record.
    """

    book = models.ForeignKey(book_models.Book, on_delete=models.PROTECT)
    isbn = models.CharField(max_length=13, default="")
    cover_image_url = models.URLField(default="")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["isbn"], condition=~Q(isbn=""), name="unique_isbn")
        ]

    def __repr__(self) -> str:
        return f"<Volume: {self.book} ({self.pk})>"

    def __str__(self) -> str:
        return self.book.title
