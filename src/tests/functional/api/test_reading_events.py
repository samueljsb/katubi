import datetime
from unittest.mock import patch

from rest_framework.test import APIClient

from katubi.books import models as book_models
from katubi.reading_events import models
from katubi.volumes.lookup import _google_books as lookup
from tests import factories


class _TestRecordReadingEvent:
    endpoint: str
    event_type: models.EventType

    def test_endpoint_requires_auth_token(self):
        client = APIClient()
        response = client.post(
            self.endpoint,
            {"title": "9780141036144", "authors": [], "date": "2021-05-12"},
            format="json",
        )

        assert response.status_code == 401

    def test_get_request_not_allowed(self, api_client):
        response = api_client.get(
            self.endpoint,
            {"isbn": "9780141036144", "date": "2021-05-12"},
            format="json",
        )

        assert response.status_code == 405

    @patch.object(lookup, "lookup_isbn", autospec=True)
    def test_creates_new_reading_event_for_new_book(
        self, mock_lookup_isbn, api_client, katubi_user
    ):
        book_info = factories.VolumeInfo(title="A Book")
        mock_lookup_isbn.return_value = book_info

        response = api_client.post(
            self.endpoint,
            {"isbn": "9780141036144", "date": "2021-05-12"},
            format="json",
        )

        assert response.status_code == 200

        # Check the response shows a helpful message.
        assert (
            response.json()
            == f"username {self.event_type.lower()} reading {book_info.title} on 2021-05-12."
        )

        # Check a book has been created.
        book = book_models.Book.objects.get()
        assert book.title == book_info.title
        assert book.subtitle == book_info.subtitle
        assert book.description == book_info.description
        assert book.authors.count() == len(book_info.authors)
        assert all(author.name in book_info.authors for author in book.authors.all())

        # Check a reading event has been created.
        reading_event = models.ReadingEvent.objects.get()
        assert reading_event.user == katubi_user
        assert reading_event.book == book
        assert reading_event.event_type == self.event_type
        assert reading_event.occurred_date == datetime.date(2021, 5, 12)

    @patch.object(lookup, "lookup_isbn", autospec=True)
    def test_creates_new_reading_event_for_existing_book(
        self, mock_lookup_isbn, api_client, katubi_user
    ):
        book = factories.Book()

        book_info = factories.VolumeInfo(
            title=book.title,
            authors=[a.name for a in book.authors.all()],
            subtitle=book.subtitle,
            description=book.description,
        )
        mock_lookup_isbn.return_value = book_info

        response = api_client.post(
            self.endpoint,
            {"isbn": "9780141036144", "date": "2021-05-12"},
            format="json",
        )

        assert response.status_code == 200

        # Check the response shows a helpful message.
        assert (
            response.json()
            == f"username {self.event_type.lower()} reading {book.title} on 2021-05-12."
        )

        # Check a reading event has been created.
        reading_event = models.ReadingEvent.objects.get()
        assert reading_event.user == katubi_user
        assert reading_event.book == book
        assert reading_event.event_type == self.event_type
        assert reading_event.occurred_date == datetime.date(2021, 5, 12)

    @patch.object(lookup, "lookup_isbn", autospec=True)
    def test_creates_ignores_existing_reading_event_for_existing_book(
        self, mock_lookup_isbn, api_client, katubi_user
    ):
        book = factories.Book()
        factories.ReadingEvent(
            user=katubi_user,
            book=book,
            event_type=self.event_type,
            occurred_date=datetime.date(2021, 5, 12),
        )

        book_info = factories.VolumeInfo(
            title=book.title,
            authors=[a.name for a in book.authors.all()],
            subtitle=book.subtitle,
            description=book.description,
        )
        mock_lookup_isbn.return_value = book_info

        response = api_client.post(
            self.endpoint,
            {"isbn": "9780141036144", "date": "2021-05-12"},
            format="json",
        )

        assert response.status_code == 200

        # Check the response shows a helpful message.
        assert (
            response.json()
            == f"username {self.event_type.lower()} reading {book.title} on 2021-05-12."
        )

    def test_returns_errors_for_invalid_data(self, api_client):
        response = api_client.post(
            self.endpoint,
            {"isbn": "97801410361444", "date": "2021-05-32"},
            format="json",
        )

        assert response.status_code == 400
        assert response.json() == {
            "isbn": ["Ensure this field has no more than 13 characters."],
            "date": [
                "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
            ],
        }

    @patch.object(lookup, "lookup_isbn", autospec=True)
    def test_returns_not_found_if_no_information_found_for_isbn(
        self, mock_lookup_isbn, api_client
    ):
        mock_lookup_isbn.side_effect = lookup.NotFound

        response = api_client.post(
            self.endpoint,
            {"isbn": "9780141036144", "date": "2021-05-12"},
            format="json",
        )

        assert response.status_code == 404
        assert response.json() == "No information found for ISBN '9780141036144'."


class TestRecordReadingStarted(_TestRecordReadingEvent):
    endpoint = "/api/record-reading-started/"
    event_type = models.EventType.STARTED


class TestRecordReadingFinished(_TestRecordReadingEvent):
    endpoint = "/api/record-reading-finished/"
    event_type = models.EventType.FINISHED
