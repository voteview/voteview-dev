import json
import os

import pytest
import tests.config

import vvtool.app


@pytest.fixture(name="db")
def _db():
    name = os.environ["VVCLI_DB_NAME"]
    db = vvtool.app.connect(name)
    yield
    db.drop_database(name)


def demo_members():
    path = tests.config.TESTS_DIR / "data" / "members.json"
    with open(path) as f:
        return json.load(f)


def demo_rollcalls():
    path = tests.config.TESTS_DIR / "data" / "rollcalls.json"
    with open(path) as f:
        return json.load(f)


def demo_persons():
    path = tests.config.TESTS_DIR / "data" / "persons.json"
    with open(path) as f:
        return json.load(f)


@pytest.fixture
def ingest(db):
    for person in demo_persons():
        vvtool.app.Person(**person).save()
