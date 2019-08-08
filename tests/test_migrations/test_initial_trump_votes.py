"""Test Trump votes migration."""

import importlib

import vvtool


MIGRATION = importlib.import_module("vvtool.migrations.0001_trump")


def test_trump_migration(db):
    """The migration appends votes to rollcalls.

    Migrating up adds votes to the selected rollcalls.
    Migrating down removes the votes.
    """

    for rollcall in MIGRATION.read_votes():
        vvtool.Rollcall(rollcall_id=rollcall["VoteviewID"]).save()

    assert list(db.voteview_rollcalls.find({"votes.icpsr": 99912})) == []

    MIGRATION.up()
    assert len(list(db.voteview_rollcalls.find({"votes.icpsr": 99912}))) > 0

    MIGRATION.down()
    assert list(db.voteview_rollcalls.find({"votes.icpsr": 99912})) == []
