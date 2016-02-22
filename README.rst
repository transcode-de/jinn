========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |requires|
        | |codecov|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/jinn/badge/?style=flat
    :target: https://readthedocs.org/projects/jinn
    :alt: Documentation Status

.. |requires| image:: https://requires.io/github/transcode-de/jinn/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/transcode-de/jinn/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/transcode-de/jinn/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/transcode-de/jinn

.. |version| image:: https://img.shields.io/pypi/v/jinn.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/jinn

.. |downloads| image:: https://img.shields.io/pypi/dm/jinn.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/jinn

.. |wheel| image:: https://img.shields.io/pypi/wheel/jinn.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/jinn

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/jinn.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/jinn

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/jinn.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/jinn


.. end-badges

A invoke wrapper.

* Free software: BSD license

Installation
============

::

    pip install jinn

Documentation
=============

https://jinn.readthedocs.org/

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
