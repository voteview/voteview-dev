"""Tests for vvtool."""

import os

import pymongo
import pymongo.database
import tests.helpers

import vvtool.app


def test_import():
    """Importing the module worked."""
    assert vvtool.app


def test_connect():
    """Connect to the database."""
    db = vvtool.app.connect(os.environ["VVCLI_DB_NAME"])
    assert isinstance(db, pymongo.database.Database)


def test_insert(db):
    """Insert a value into the database."""
    tests.helpers.run(["insert", "rollcall", "-qid=RS99912345"])
    result = list(db.voteview_rollcalls.find_all({}))
    assert result == [{"id": "RS99912345"}]
