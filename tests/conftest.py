"""Test setup module.

PyTest executes this at the beginning of a test sesion."""

import json
import os

import pytest
import tests.config

import vvtool.app


@pytest.fixture(name="db")
def _db():
    """Access the database specified by the VVCLI_DB_NAME environment variable."""
    name = os.environ["VVCLI_DB_NAME"]
    conn = vvtool.app.connect(name)
    yield
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
def ingest(db):  # pylint: disable=unused-argument,invalid-name
    """Load all data from the demo files into the database."""
    for person in demo_persons():
        vvtool.app.Person(**person).save()

    for member in demo_members():
        vvtool.app.Member(**member).save()

    for rollcall in demo_rollcalls():
        vvtool.app.Rollcall(**rollcall).save()
