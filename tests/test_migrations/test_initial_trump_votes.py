import importlib

import pymongo

import vvtool


trump_migration = importlib.import_module("vvtool.migrations.0001_trump")


def test_trump(db):

    for rollcall in trump_migration.read_votes():
        vvtool.Rollcall(rollcall_id=rollcall["VoteviewID"]).save()

    assert list(db.voteview_rollcalls.find({"votes.icpsr": 99912})) == []

    trump_migration.up()
    assert len(list(db.voteview_rollcalls.find({"votes.icpsr": 99912}))) > 0

    trump_migration.down()
    assert list(db.voteview_rollcalls.find({"votes.icpsr": 99912})) == []
