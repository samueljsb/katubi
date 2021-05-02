import pytest
import responses

from katubi import lookup


class TestLookupISBN:
    def test_raises_if_no_books_found(self, json_fixture):
        with responses.RequestsMock() as mock_responses:
            mock_responses.add(
                method="GET",
                url="https://www.googleapis.com/books/v1/volumes",
                json=json_fixture("google_books_api/isbn_invalid.json"),
            )

            with pytest.raises(lookup.NotFound):
                lookup.lookup_isbn("1234567890123")

    def test_returns_book_info(self, json_fixture):
        with responses.RequestsMock() as mock_responses:
            mock_responses.add(
                method="GET",
                url="https://www.googleapis.com/books/v1/volumes",
                json=json_fixture("google_books_api/isbn_valid.json"),
            )

            book_info = lookup.lookup_isbn("1234567890123")

        assert book_info == lookup.BookInfo(
            title="Scarcity",
            subtitle="The True Cost of Not Having Enough",
            authors=["Sendhil Mullainathan", "Eldar Shafir"],
            description="Why can we never seem to keep on top of our workload, social diary or chores? ...",
            image_url="http://books.google.com/books/content?id=bKapoAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api",
        )

    def test_returns_book_info_when_data_is_missing(self, json_fixture):
        with responses.RequestsMock() as mock_responses:
            mock_responses.add(
                method="GET",
                url="https://www.googleapis.com/books/v1/volumes",
                # Return a valid volume with all the data we want missing.
                json=json_fixture("google_books_api/isbn_valid_missing_data.json"),
            )

            book_info = lookup.lookup_isbn("1234567890123")

        assert book_info == lookup.BookInfo(
            title="",
            subtitle="",
            authors=[],
            description="",
            image_url=None,
        )

    def test_query_string_is_correct(self, json_fixture):
        with responses.RequestsMock() as mock_responses:
            mock_responses.add(
                method="GET",
                url="https://www.googleapis.com/books/v1/volumes",
                json=json_fixture("google_books_api/isbn_valid.json"),
            )

            lookup.lookup_isbn("1234567890123")

            assert mock_responses.calls[0].request.url.endswith(
                "?q=isbn%3A1234567890123&maxResults=1"
            )
