import datetime

from django.contrib.auth import models as auth_models

from katubi import logging
from katubi.books import models as book_models
from katubi.reading_events import models, operations
from katubi.volumes import lookup as volume_lookup

logger = logging.get_logger("reading_events")


class CannotRecordReadingEvent(Exception):
    """
    The reading event cannot be recorded.
    """


def record_reading_started_from_isbn(
    *, isbn: str, date: datetime.date, user: auth_models.User
) -> models.ReadingEvent:
    """
    Record a reading started event.

    Args:
        isbn:   The isbn of the volume that the user has started to read.
        date:   The date the user started to read the volume.
        user:   The user that is reading.

    Raises CannotRecordReadingEvent if no information could be found for this ISBN.
    """
    book = _get_book_for_isbn(isbn)

    reading_event = operations.record_reading_event(
        user=user,
        book=book,
        event_type=models.EventType.STARTED,
        occurred_date=date,
    )

    logger.info(
        "Recorded reading started",
        params={"isbn": isbn, "date": date.isoformat(), "user_id": user.id},
        metadata={
            "reading_event_id": reading_event.id,
            "book_title": reading_event.book.title,
        },
    )

    return reading_event


def record_reading_finished_from_isbn(
    *, isbn: str, date: datetime.date, user: auth_models.User
) -> models.ReadingEvent:
    """
    Record a reading finished event.

    Args:
        isbn:   The isbn of the volume that the user has finished reading.
        date:   The date the user finished reading the volume.
        user:   The user that is reading.

    Raises CannotRecordReadingEvent if no information could be found for this ISBN.
    """
    book = _get_book_for_isbn(isbn)

    reading_event = operations.record_reading_event(
        user=user,
        book=book,
        event_type=models.EventType.FINISHED,
        occurred_date=date,
    )

    logger.info(
        "Recorded reading finished",
        params={"isbn": isbn, "date": date.isoformat(), "user_id": user.id},
        metadata={
            "reading_event_id": reading_event.id,
            "book_title": reading_event.book.title,
        },
    )

    return reading_event


def _get_book_for_isbn(isbn: str) -> book_models.Book:
    try:
        volume, __ = volume_lookup.get_or_create_volume_for_isbn(isbn)
    except volume_lookup.NotFound:
        raise CannotRecordReadingEvent(f"No information found for ISBN '{isbn}'.")

    return volume.book
