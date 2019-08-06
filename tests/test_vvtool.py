"""Tests for vvtool."""

import os

import pymongo
import pymongo.database
import tests.helpers

import vvtool.app


def test_import():
    """Importing the module worked."""
    assert vvtool.app


def test_ingest(ingest):
    """The ``ingest`` fixture puts data into the database."""
    [person] = set(vvtool.app.Person.objects(bioname="ADAMS, Alma"))
    assert person.born == 1946

    [member] = vvtool.app.Member.objects(party_code=100)
    assert member.congress == 116

    [rollcall] = vvtool.app.Rollcall.objects(rollnumber=85)
    assert rollcall.congress == 116
