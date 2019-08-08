"""Test setup module.

PyTest executes this at the beginning of a test sesion.
"""

import json
import os

import pytest
import tests.config

import vvtool.app


@pytest.fixture(name="client")
def _client():
    """Access the database specified by the VVCLI_DB_NAME environment variable."""
    name = os.environ["VVCLI_DB_NAME"]
    port = int(os.environ.get("MONGO_27017_TCP", 27017))
    conn = vvtool.app.connect(name, port=port)
    yield conn
    conn.drop_database(name)


def demo_members():
    """Load members from the demo file."""
    path = tests.config.TESTS_DIR / "data" / "members.json"
    with open(path) as file:
        return json.load(file)


def demo_rollcalls():
    """Load rollcalls from the demo file."""
    path = tests.config.TESTS_DIR / "data" / "rollcalls.json"
    with open(path) as file:
        return json.load(file)


def demo_persons():
    """Load persons from the demo file."""
    path = tests.config.TESTS_DIR / "data" / "persons.json"
    with open(path) as file:
        return json.load(file)


@pytest.fixture
def ingest(client):  # pylint: disable=unused-argument,invalid-name
    """Load all data from the demo files into the database."""
    for person in demo_persons():
        vvtool.app.Person(**person).save()

    for member in demo_members():
        vvtool.app.Member(**member).save()

    for rollcall in demo_rollcalls():
        vvtool.app.Rollcall(**rollcall).save()


@pytest.fixture(name="db")
def _db(client):
    name = os.environ["VVCLI_DB_NAME"]
    yield client[name]
    client.drop_database(name)
