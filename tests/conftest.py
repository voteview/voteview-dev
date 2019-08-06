import os

import pytest

import vvtool.app


@pytest.fixture(name="db")
def _db():
    return vvtool.app.connect(os.environ["VVCLI_DB_NAME"])
