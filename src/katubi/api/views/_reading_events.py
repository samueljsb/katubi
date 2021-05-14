from django.http import Http404
from rest_framework import request, serializers

from katubi import lookup
from katubi.application import commands
from katubi.application.types import Command
from katubi.books import queries as book_queries

from . import _base as base


class RecordReadingEventFromISBNSerializer(serializers.Serializer):
    isbn = serializers.CharField(max_length=13)
    date = serializers.DateField()


class RecordReadingStartedFromISBN(base.CommandView):
    """
    View to record a reading started event.

    The book that is being read is determined from the isbn.
    """

    Serializer = RecordReadingEventFromISBNSerializer

    def get_commands(self, request: request.Request, data: dict) -> list[Command]:
        # Get or create the book.
        try:
            book, __ = book_queries.get_or_create_from_isbn(data["isbn"])
        except lookup.NotFound:
            raise Http404(f"No book found with ISBN {data['isbn']}")

        command = commands.RecordReadingStarted(
            user=request.user, book=book, started_date=data["date"]
        )
        return [command]


class RecordReadingFinishedFromISBN(base.CommandView):
    """
    View to record a reading finished event.

    The book that is being read is determined from the isbn.
    """

    Serializer = RecordReadingEventFromISBNSerializer

    def get_commands(self, request: request.Request, data: dict) -> list[Command]:
        # Get or create the book.
        try:
            book, __ = book_queries.get_or_create_from_isbn(data["isbn"])
        except lookup.NotFound:
            raise Http404(f"No book found with ISBN {data['isbn']}")

        command = commands.RecordReadingFinished(
            user=request.user, book=book, finished_date=data["date"]
        )
        return [command]
