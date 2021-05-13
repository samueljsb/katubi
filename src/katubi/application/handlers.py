from katubi.reading_events import models as reading_event_models

from . import commands
from .types import Message


def record_reading_started(
    command: commands.RecordReadingStarted, queue: list[Message]
) -> None:
    """
    Record a STARTED reading event.
    """
    reading_event_models.ReadingEvent.new(
        user=command.user,
        book=command.book,
        event_type=reading_event_models.EventType.STARTED,
        occurred_date=command.started_date,
    )


def record_reading_finished(
    command: commands.RecordReadingFinished, queue: list[Message]
) -> None:
    """
    Record a FINISHED reading event.
    """
    reading_event_models.ReadingEvent.new(
        user=command.user,
        book=command.book,
        event_type=reading_event_models.EventType.FINISHED,
        occurred_date=command.finished_date,
    )
