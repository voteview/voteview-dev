"""Test vvtool command-line interface."""

import importlib
import subprocess

import vvtool


MIGRATION = importlib.import_module("vvtool.migrations.0001_trump")


def run(db, args, **kwargs):
    """Run vvtool as a subprocess."""
    host, port = db.client.address

    cli_args = ["-d", db.name, "--host", host, "--port", str(port)]
    check = kwargs.pop("check", True)
    executable = "vvtool"
    return subprocess.run(
        [executable] + list(args) + cli_args,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **kwargs
    )


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
    run(db, ["migration", "up", "1"])

    # Then:
    # Trump's votes appear in the database.
    assert len(list(db.voteview_rollcalls.find({"votes.icpsr": 99912}))) > 0

    # When:
    # Do the down migration.
    run(db, ["migration", "down", "1"])

    # Then:
    # Trump's votes don't appear in the database.
    assert list(db.voteview_rollcalls.find({"votes.icpsr": 99912})) == []


def test_status_empty(db, tmp_path):
    """The status command shows migrations that haven't been executed."""

    # Given:
    # An empty migrations/ directory.
    (tmp_path / "migrations").mkdir()

    # Then:
    # No migrations are shown.
    output = run(db, ["migration", "--path", str(tmp_path), "status"])
    assert "All migrations registered" in output.stderr.decode()

    # When:
    # Create a migration.
    run(db, ["migration", "--path", str(tmp_path), "create", "first_migration"])

    # Then:
    # The migration apepars in the status output.
    output = run(db, ["migration", "--path", str(tmp_path), "status"]).stderr
    assert "first_migration" in output.decode()

    # When:
    # Execute the migration.
    run(db, ["migration", "--path", str(tmp_path), "up", "1"])

    # Then:
    # All migrations have been registered.
    output = run(db, ["migration", "--path", str(tmp_path), "status"]).stderr
    assert "All migrations registered" in output.decode()
