=====
Usage
=====

Create a migration by running ``vvtool`` on the command line:

.. code-block:: bash

   $ poetry install
   ...

   $ poetry run vvtool migrate create add_votes



This will create a new migration file under ``migrations``. Write code for doing
the migration upgrade in the ``up`` function and for reverting it in the
``down`` function. See ``0001_trump.py`` for an example.



.. code-block:: python

    """Add initial Trump votes from Congressional Quarterly file."""


    import csv
    import typing as t

    import importlib_resources

    import vvtool.migrations.data


    DATA_FILE = "initial_trump_votes.csv"
    TRUMP_ICPSR = 99912


    def read_votes() -> t.List[t.Dict[str, str]]:
        """Read Trump vote records from the data file."""
        with importlib_resources.open_text(vvtool.migrations.data, DATA_FILE) as file:
            return list(csv.DictReader(file))


    def up(db=None):  # pylint: disable=unused-argument
        """Add initial Trump votes from Congressional Quarterly file."""
        for record in read_votes():
            rollcall = vvtool.Rollcall.objects(rollcall_id=record["VoteviewID"])
            new_vote = {"icpsr": TRUMP_ICPSR, "cast_code": 1}
            rollcall.update_one(push__votes=new_vote)


    def down(db=None):  # pylint: disable=unused-argument
        """Remove initial Trump votes from Congressional Quarterly file."""
        for trump_vote in read_votes():
            rollcall = vvtool.Rollcall.objects(rollcall_id=trump_vote["VoteviewID"])
            new_vote = {"icpsr": TRUMP_ICPSR, "cast_code": 1}
            rollcall.update_one(pull__votes=new_vote)



Also write a test that
it works. See ``test_initial_trump_votes.py`` for an example.


.. code-block:: python

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



To change the date of a rollcall, filter the rollcall objects, and ``update()``
with the new data. In the database, ``id`` is the field containing the
human-readable identifier for rollcalls and members. However, ``mongoengine``
treats ``id`` as a reserved name, so we have to use ``rollcall_id`` instead when
querying through the ``Rollcall.object()`` API.



To run the tests, install docker and run tox.

.. code-block:: bash

    $ tox


When you're satisfied that the migration works, run the migration on a database. Use the id number of the migration.


If you have ``vvtool`` installed, run migration ``0001`` by executing:

.. code-block:: bash

     $  vvtool migrate -d voteview up 1


Check that it worked.
