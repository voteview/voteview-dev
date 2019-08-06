========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/vvtool/badge/?style=flat
    :target: https://readthedocs.org/projects/vvtool
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/voteview/vvtool.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/voteview/vvtool

.. |version| image:: https://img.shields.io/pypi/v/voteview.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/pypi/voteview

.. |commits-since| image:: https://img.shields.io/github/commits-since/voteview/vvtool/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/voteview/vvtool/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/voteview.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/pypi/voteview

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/voteview.svg
    :alt: Supported versions
    :target: https://pypi.org/pypi/voteview

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/voteview.svg
    :alt: Supported implementations
    :target: https://pypi.org/pypi/voteview


.. end-badges

Voteview command-line interface.

* Free software: GNU General Public License v3 (GPLv3)

Installation
============

::

    pip install voteview

Documentation
=============


https://vvtool.readthedocs.io/


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
