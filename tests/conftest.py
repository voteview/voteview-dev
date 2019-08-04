import os

import pytest

import vvcli.app


@pytest.fixture(name="db")
def _db():
    return vvcli.app.connect(os.environ["VVCLI_DB_NAME"])
