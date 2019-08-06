"""Tests for vvtool."""

import datetime

import pytest

import vvtool.app


def test_import():
    """Importing the module worked."""
    assert vvtool.app


@pytest.mark.usefixtures("ingest")
def test_ingest():
    """The ``ingest`` fixture puts data into the database."""
    [person] = set(vvtool.app.Person.objects(bioname="ADAMS, Alma"))
    assert person.born == 1946

    [member] = vvtool.app.Member.objects(party_code=100)
    assert member.congress == 116

    [rollcall] = vvtool.app.Rollcall.objects(rollnumber=85)
    assert rollcall.congress == 116


@pytest.mark.usefixtures("ingest")
def test_update_rollcall_date():
    """Updating a rollcall date is visible afterwards."""

    initial = datetime.date(2019, 2, 14)
    [rollcall] = vvtool.app.Rollcall.objects(rollnumber=85)
    assert rollcall.date == initial

    new = datetime.date(2019, 1, 1)
    vvtool.app.Rollcall.objects(rollcall_id="RH1160085").update(date=new)
    [rollcall] = vvtool.app.Rollcall.objects(rollnumber=85)
    assert rollcall.date == new
