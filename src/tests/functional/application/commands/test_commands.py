import datetime

from katubi.application import commands, message_bus
from katubi.reading_events import models as reading_event_models
from tests import factories


def test_record_reading_started():
    user = factories.User()
    book = factories.Book()

    # Queue the command to record the reading and handle it.
    command = commands.RecordReadingStarted(
        user=user, book=book, started_date=datetime.date(2021, 5, 2)
    )
    message_bus.handle([command])

    # Check a single reading started event has been recorded.
    event = reading_event_models.ReadingEvent.objects.get()
    assert event.user == user
    assert event.book == book
    assert event.occurred_date == datetime.date(2021, 5, 2)
    assert event.event_type == reading_event_models.EventType.STARTED


def test_record_reading_finished():
    user = factories.User()
    book = factories.Book()

    # Queue the command to record the reading and handle it.
    command = commands.RecordReadingFinished(
        user=user, book=book, finished_date=datetime.date(2021, 5, 2)
    )
    message_bus.handle([command])

    # Check a single reading finished event has been recorded.
    event = reading_event_models.ReadingEvent.objects.get()
    assert event.user == user
    assert event.book == book
    assert event.occurred_date == datetime.date(2021, 5, 2)
    assert event.event_type == reading_event_models.EventType.FINISHED
