"""Tests for vvtool."""

import datetime

import pytest

import vvtool.application
import vvtool.documents


def test_import():
    """Importing the module worked."""
    assert vvtool.application


@pytest.mark.usefixtures("ingest")
def test_ingest():
    """The ``ingest`` fixture puts data into the database."""
    [person] = set(vvtool.documents.Person.objects(bioname="ADAMS, Alma"))
    assert person.born == 1946

    [member] = vvtool.documents.Member.objects(party_code=100)
    assert member.congress == 116

    [rollcall] = vvtool.documents.Rollcall.objects(rollnumber=85)
    assert rollcall.congress == 116


@pytest.mark.usefixtures("ingest")
def test_update_rollcall_date():
    """Updating a rollcall date is visible afterwards."""

    initial = datetime.date(2019, 2, 14)
    [rollcall] = vvtool.documents.Rollcall.objects(rollnumber=85)
    assert rollcall.date == initial

    new = datetime.date(2019, 1, 1)
    vvtool.documents.Rollcall.objects(rollcall_id="RH1160085").update(date=new)
    [rollcall] = vvtool.documents.Rollcall.objects(rollnumber=85)
    assert rollcall.date == new
