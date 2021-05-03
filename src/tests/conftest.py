import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent.absolute() / "fixtures"


def pytest_collection_modifyitems(config, items):
    # Loop over each test and add the appropriate marks, inferred from the location of
    # the test module.
    for item in items:
        filepath = str(item.fspath)

        # Ensure all integration and functional tests are run with DB marker
        if "tests/integration" in filepath or "tests/functional" in filepath:
            # It's possible the marker may already be there if the test requires
            # database transaction support.
            if "django_db" not in [m.name for m in item.own_markers]:
                item.add_marker(pytest.mark.django_db)


@pytest.fixture
def json_fixture():
    """
    Load JSON data from a fixture file.
    """

    def json_fixture(fixture_path):
        filepath = FIXTURES_DIR / fixture_path
        return json.load(filepath.open())

    return json_fixture
