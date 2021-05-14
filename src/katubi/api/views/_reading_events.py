import datetime
from typing import Tuple

from django.http import Http404
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from katubi import lookup
from katubi.application import commands, message_bus
from katubi.books import models as book_models
from katubi.books import queries as book_queries


class RecordReadingEventFromISBNSerializer(serializers.Serializer):
    isbn = serializers.CharField(max_length=13)
    date = serializers.DateField()


class _RecordReadingEventFromISBN(APIView):
    """
    View to record a reading event.

    The book that is being read is determined from the ISBN.
    """

    def get_data(self, request: Request) -> Tuple[book_models.Book, datetime.date]:
        # Deserialize and validate the input data.
        serializer = RecordReadingEventFromISBNSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated data.
        isbn = serializer.validated_data["isbn"]
        event_date = serializer.validated_data["date"]

        # Get or create the book.
        try:
            book, __ = book_queries.get_or_create_from_isbn(isbn)
        except lookup.NotFound:
            raise Http404(f"No book found with ISBN {isbn}")

        return book, event_date


class RecordReadingStartedFromISBN(_RecordReadingEventFromISBN):
    """
    View to record a reading started event.

    The book that is being read is determined from the isbn.
    """

    def post(self, request: Request) -> Response:
        # Deserialize and validate the input data.
        book, event_date = self.get_data(request)

        # Record the reading event.
        command = commands.RecordReadingStarted(
            user=request.user, book=book, started_date=event_date
        )
        message_bus.handle([command])

        return Response()


class RecordReadingFinishedFromISBN(_RecordReadingEventFromISBN):
    """
    View to record a reading finished event.

    The book that is being read is determined from the isbn.
    """

    def post(self, request: Request) -> Response:
        # Deserialize and validate the input data.
        book, event_date = self.get_data(request)

        # Record the reading event.
        command = commands.RecordReadingFinished(
            user=request.user,
            book=book,
            finished_date=event_date,
        )
        message_bus.handle([command])

        return Response()
