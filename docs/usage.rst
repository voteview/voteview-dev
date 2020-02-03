=====
Usage
=====


.. note::

   All steps are expected to be performed on your local computer, not the target database
   server.


Creating migrations
---------------------------

Create a migration by running ``vvtool`` on the command line:

.. code-block:: bash

   $ poetry install
   ...

   $ poetry run vvtool --database voteview migration create add_votes



This will create a new migration file under ``migrations``. Write code for doing
the migration upgrade in the ``up`` function and for reverting it in the
``down`` function. See ``0001_trump.py`` for an example.


.. literalinclude:: ../src/vvtool/migrations/0001_trump.py
   :language: python

Also write a test that
it works. See ``test_initial_trump_votes.py`` for an example.


.. literalinclude:: ../tests/test_migrations/test_initial_trump_votes.py
   :language: python


To change the date of a rollcall, filter the rollcall objects, and ``update()``
with the new data. In the database, ``id`` is the field containing the
human-readable identifier for rollcalls and members. However, ``mongoengine``
treats ``id`` as a reserved name, so we have to use ``rollcall_id`` instead when
querying through the ``Rollcall.object()`` API.



To run the tests, install docker and run tox.

.. code-block:: bash

    $ poetry run tox



When you're satisfied that the migration works,

* Add your change in the changelog.
* Create a pull request into ``master``.




Execution
-----------

In another terminal, set up ssh forwarding for the staging database server. Plug in the
address or ssh alias of the staging server. Connections to the local MongoDB port will be
forwarded to the remote MongoDB port.


.. code-block:: bash

   % ssh -NL 27017:localhost:27017 "${STAGING_SERVER}"


Find the id number of the migration to execute.

.. code-block:: bash

    % vvtool migration status --host localhost --database=voteview

Note this ``localhost`` is really the staging server because of ssh forwarding.



Run the migration using the id number. For example, to upgrade through migration number
``0001``, run:

.. code-block:: bash

     %  vvtool migration up --host=localhost --database=voteview 1
