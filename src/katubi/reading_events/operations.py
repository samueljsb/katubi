import datetime

from django.contrib.auth import models as auth_models

from katubi.books import models as book_models

from . import models


def record_reading_event(
    *,
    user: auth_models.User,
    book: book_models.Book,
    event_type: models.EventType,
    occurred_date: datetime.date,
) -> models.ReadingEvent:
    """
    Record a new reading event.
    """
    return models.ReadingEvent.objects.create(
        user=user, book=book, event_type=event_type, occurred_date=occurred_date
    )
