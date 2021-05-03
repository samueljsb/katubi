import datetime
from dataclasses import dataclass

from django.contrib.auth import models as auth_models

from katubi.books import models as book_models

from . import _base as base


@dataclass(frozen=True)
class RecordReadingStarted(base.Command):
    """
    Record that a user has started reading a book.
    """

    user: auth_models.User
    book: book_models.Book
    started_date: datetime.date


@dataclass(frozen=True)
class RecordReadingFinished(base.Command):
    """
    Record that a user has finished reading a book.
    """

    user: auth_models.User
    book: book_models.Book
    finished_date: datetime.date
