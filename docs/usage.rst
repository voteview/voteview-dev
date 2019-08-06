=====
Usage
=====

To change the date of a rollcall, filter the rollcall objects, and ``update()``
with the new data. In the database, ``id`` is the field containing the
human-readable identifier for rollcalls and members. However, ``mongoengine``
treats ``id`` as a reserved name, so we have to use ``rollcall_id`` instead when
querying through the ``Rollcall.object()`` API.

.. code-block:: python

        import datetime

	import vvtool

        # Connect to the database.
        vvtool.connect('voteview')

        # Find the matching rollcall.
        original = vvtool.Rollcall.objects(rollcall_id='RS1160085')

        # Define the new date for the rollcall.
        new = datetime.date(2020, 1, 1)

        # Update the rollcall with the new date.
        original.update(date=new)

        # Check that it worked.
        [rollcall] = vvtool.Rollcall.objects(rollnumber=85)
        assert rollcall.date == new
