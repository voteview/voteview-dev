========
vvtool
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/voteview-dev/badge/?style=flat
    :target: https://readthedocs.org/projects/voteview-dev
    :alt: Documentation Status


.. |travis| image:: https://img.shields.io/travis/com/voteview/voteview-dev/master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/voteview/voteview-dev

.. |version| image:: https://img.shields.io/pypi/v/voteview-dev.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/voteview-dev

.. |commits-since| image:: https://img.shields.io/github/commits-since/voteview/voteview-dev/v0.1.5.svg
    :alt: Commits since latest release
    :target: https://github.com/voteview/voteview-dev/compare/v0.1.5...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/voteview-dev.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/voteview-dev

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/voteview-dev.svg
    :alt: Supported versions
    :target: https://pypi.org/project/voteview-dev

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/voteview-dev.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/voteview-dev


.. end-badges

This project contains tools for managing the Voteview server.


Any manual changes to the database contents can be applied through this tool.


What's good
-------------

The advantages of using ``vvtool``:

- All migrations are versioned.
- All migrations can be programatically applied and reverted.
- All migrations are documented in the changelog.
- All migrations can be developed and tested on the user's local computer instead of running
  for the first time in production.
- The representation of database objects can be standardized: vvtool defines a set of
  attributes for ``Member``, ``Rollcall``, and other objects.
- Any changes to software or migrations can be tested automatically on a `continuous
  integration server`_.
- The software can be `documented centrally <docs>`_ instead of using scattered shell scripts.
- ``vvtool`` connects directly to a test database or the production database,
  reducing the differences between the test environment and the production environment.


What's bad
-----------

- Requires a few setup steps.
- Doesn't **require** changes to go through continuous integration testing, since users
  can submit jobs directly to the target server. So it's possible that a script could be
  executed without ever being tested. This shortcoming could be changed by swiching to a
  continuous **deployment** strategy whereby users would simply submit migrations to
  GitHub, wait for them to go through testing, and then the migrations would be
  automatically applied to the production database. The current situation is much simpler,
  so I've stuck with that for now.

Documentation
=============

https://voteview-dev.readthedocs.io/



.. _continuous integration server: https://travis-ci.com/voteview/voteview-dev
.. _docs: https://voteview-dev.readthedocs.io/
