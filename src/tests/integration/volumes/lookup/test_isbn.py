from unittest import mock

import pytest

from katubi.volumes.lookup import _google_books as google_books
from katubi.volumes.lookup import _isbn as isbn_lookup
from tests import factories


class TestGetOrCreateVolumeForIsbn:
    def test_retrieves_existing_volume(self):
        existing_volume = factories.Volume(isbn="9780141049199")

        volume, created = isbn_lookup.get_or_create_volume_for_isbn("978-0-14-104919-9")

        assert volume == existing_volume
        assert created is False

    @mock.patch.object(google_books, "lookup_isbn")
    def test_creates_new_volume_for_existing_book(self, lookup_isbn):
        # Create an existing book record and make sure the Google Books module returns
        # information that matches this book.
        existing_book = factories.Book(
            title="A Book",
            authors=[
                factories.Author(name="T Author"),
                factories.Author(name="A N Other"),
            ],
        )
        lookup_isbn.return_value = factories.VolumeInfo(
            title="A Book",
            authors=["T Author", "A N Other"],
            image_url="https://example,com/image.png",
        )

        volume, created = isbn_lookup.get_or_create_volume_for_isbn("978-0-14-104919-9")

        assert created is True
        assert volume.book == existing_book
        assert volume.isbn == "9780141049199"  # unmasked
        assert volume.cover_image_url == "https://example,com/image.png"

    @mock.patch.object(google_books, "lookup_isbn")
    def test_creates_new_volume_for_new_book(self, lookup_isbn):
        lookup_isbn.return_value = factories.VolumeInfo(
            title="A Book",
            authors=["T Author", "A N Other"],
            image_url="https://example,com/image.png",
        )

        volume, created = isbn_lookup.get_or_create_volume_for_isbn("978-0-14-104919-9")

        assert created is True
        assert volume.book.title == "A Book"
        assert set(volume.book.authors.values_list("name", flat=True)) == {
            "T Author",
            "A N Other",
        }
        assert volume.isbn == "9780141049199"  # unmasked
        assert volume.cover_image_url == "https://example,com/image.png"

    @mock.patch.object(google_books, "lookup_isbn")
    def test_raises_if_no_info_found_for_isbn(self, lookup_isbn):
        lookup_isbn.side_effect = google_books.NotFound

        with pytest.raises(google_books.NotFound):
            isbn_lookup.get_or_create_volume_for_isbn("978-0-14-104919-9")

    @mock.patch.object(google_books, "lookup_isbn")
    def test_invalid_isbn_raises_not_found(self, lookup_isbn):
        # Make Google Books return a volume so we know that isn't why the method raises.
        lookup_isbn.return_value = factories.VolumeInfo(
            title="A Book",
            authors=["T Author", "A N Other"],
            image_url="https://example,com/image.png",
        )

        with pytest.raises(google_books.NotFound):
            isbn_lookup.get_or_create_volume_for_isbn("invalid-isbn")
