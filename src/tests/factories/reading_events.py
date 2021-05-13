import factory
from django.utils import timezone

from katubi.reading_events import models

from . import auth, books


class ReadingEvent(factory.django.DjangoModelFactory):
    user = factory.SubFactory(auth.User)
    book = factory.SubFactory(books.Book)
    occurred_date = factory.LazyFunction(timezone.now)

    class Meta:
        model = models.ReadingEvent


class StartedReadingEvent(ReadingEvent):
    event_type = models.EventType.STARTED


class FinishedReadingEvent(ReadingEvent):
    event_type = models.EventType.FINISHED
