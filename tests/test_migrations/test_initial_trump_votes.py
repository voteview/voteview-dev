"""Test Trump votes migration."""

import importlib

import vvtool


MIGRATION = importlib.import_module("vvtool.migrations.0001_trump")


def test_trump_migration(db):
    """The migration appends votes to rollcalls.

    Migrating up adds votes to the selected rollcalls.
    Migrating down removes the votes.
    """

    # Given:
    # The rollcalls on which Trump voted exist.
    for rollcall in MIGRATION.read_votes():
        vvtool.Rollcall(rollcall_id=rollcall["VoteviewID"]).save()

    # Trump has not voted.
    assert list(db.voteview_rollcalls.find({"votes.icpsr": 99912})) == []

    # When:
    # Execute the migration.
    MIGRATION.up()

    # Then:
    # Trump's votes appear in the database.
    assert len(list(db.voteview_rollcalls.find({"votes.icpsr": 99912}))) > 0

    # When:
    # Undo the migration.
    MIGRATION.down()

    # Then:
    # Trump's votes are gone from the database.
    assert list(db.voteview_rollcalls.find({"votes.icpsr": 99912})) == []
