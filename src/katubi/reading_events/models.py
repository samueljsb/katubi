from __future__ import annotations

from django.contrib.auth import models as auth_models
from django.db import models

from katubi.books import models as book_models


class EventType(models.TextChoices):
    STARTED = "STARTED"
    FINISHED = "FINISHED"


class ReadingEvent(models.Model):
    user = models.ForeignKey(auth_models.User, on_delete=models.PROTECT)
    book = models.ForeignKey(book_models.Book, on_delete=models.PROTECT)

    event_type = models.CharField(max_length=100, choices=EventType.choices)
    occurred_date = models.DateField()

    # Audit field
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return (
            f"<ReadingEvent: {self.event_type.lower()} reading {self.book.title} on "
            f"{self.occurred_date} ({self.pk})>"
        )
