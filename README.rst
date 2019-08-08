========
Overview
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


.. |travis| image:: https://img.shields.io/travis/voteview/voteview-dev/master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/voteview/voteview-dev

.. |version| image:: https://img.shields.io/pypi/v/voteview-dev.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/pypi/voteview-dev

.. |commits-since| image:: https://img.shields.io/github/commits-since/voteview/voteview-dev/v0.1.2.svg
    :alt: Commits since latest release
    :target: https://github.com/voteview/voteview-dev/compare/v0.1.2...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/voteview-dev.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/pypi/voteview-dev

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/voteview-dev.svg
    :alt: Supported versions
    :target: https://pypi.org/pypi/voteview-dev

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/voteview-dev.svg
    :alt: Supported implementations
    :target: https://pypi.org/pypi/voteview-dev


.. end-badges

Voteview command-line interface.

* Free software: GNU General Public License v3 (GPLv3)

Installation
============

::

    pip install voteview-dev

Documentation
=============


https://voteview-dev.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
