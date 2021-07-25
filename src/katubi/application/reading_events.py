import datetime

from django.contrib.auth import models as auth_models

from katubi.reading_events import models


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
    pass


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
    pass
