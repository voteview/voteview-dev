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
``down`` function. See ``0001_trump.py`` for an example. Also write a test that
it works. See ``test_initial_trump_votes.py`` for an example.


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
