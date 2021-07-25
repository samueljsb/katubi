import datetime
from unittest import mock

import pytest

from katubi.application import reading_events
from katubi.reading_events import models
from katubi.volumes import lookup
from tests import factories


class TestRecordReadingStartedFromISBN:
    def test_happy_path(self):
        user = factories.User()
        volume = factories.Volume(isbn="9780141049199")
        today = datetime.date.today()

        reading_event = reading_events.record_reading_started_from_isbn(
            isbn="9780141049199", user=user, date=today
        )

        assert reading_event.user == user
        assert reading_event.book == volume.book
        assert reading_event.occurred_date == today
        assert reading_event.event_type == models.EventType.STARTED

    @mock.patch.object(lookup, "get_or_create_volume_for_isbn")
    def test_raises_if_cannot_find_volume_for_isbn(self, get_or_create_volume_for_isbn):
        get_or_create_volume_for_isbn.side_effect = lookup.NotFound

        with pytest.raises(reading_events.CannotRecordReadingEvent):
            reading_events.record_reading_started_from_isbn(
                isbn="9780141049199", user=factories.User(), date=datetime.date.today()
            )


class TestRecordReadingFinishedFromISBN:
    def test_happy_path(self):
        user = factories.User()
        volume = factories.Volume(isbn="9780141049199")
        today = datetime.date.today()

        reading_event = reading_events.record_reading_finished_from_isbn(
            isbn="9780141049199", user=user, date=today
        )

        assert reading_event.user == user
        assert reading_event.book == volume.book
        assert reading_event.occurred_date == today
        assert reading_event.event_type == models.EventType.FINISHED

    @mock.patch.object(lookup, "get_or_create_volume_for_isbn")
    def test_raises_if_cannot_find_volume_for_isbn(self, get_or_create_volume_for_isbn):
        get_or_create_volume_for_isbn.side_effect = lookup.NotFound

        with pytest.raises(reading_events.CannotRecordReadingEvent):
            reading_events.record_reading_finished_from_isbn(
                isbn="9780141049199", user=factories.User(), date=datetime.date.today()
            )
