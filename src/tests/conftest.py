import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent.absolute() / "fixtures"


@pytest.fixture
def json_fixture():
    """
    Load JSON data from a fixture file.
    """

    def json_fixture(fixture_path):
        filepath = FIXTURES_DIR / fixture_path
        return json.load(filepath.open())

    return json_fixture
