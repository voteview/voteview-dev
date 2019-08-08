import subprocess


def run(args, **kwargs):
    """Run vvtool as a subprocess."""
    return subprocess.check_output(["vvtool"] + args, **kwargs)


def test_migrate_cli(db):
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
    run(["migrate", "-d", db.name, "up", "0001_trump"])

    # Then:
    # Trump's votes appear in the database.
    assert len(list(db.voteview_rollcalls.find({"votes.icpsr": 99912}))) > 0

    # When:
    # Do the down migration.
    run(["migrate", "-d", db.name, "down", "base"])

    # Then:
    # Trump's votes don't appear in the database.
    assert list(db.voteview_rollcalls.find({"votes.icpsr": 99912})) == []
