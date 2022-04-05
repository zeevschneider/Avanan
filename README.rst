========
Overview
========

Home assignment for Avanan

Installation
============

::

  git clone git@github.com:Traiana/Avanan.git


Documentation
=============

TODO

Usage
=====

To run the all tests run::

  tox


To run all the tests in CI environment (output a nice HTML report in
``output/pytest``) run::

  tox -e ci


Development
===========

For a more efficient and direct development environment - you should install all
dependencies directly into your virtual environment::

  pip3 install -r requirements-dev.txt

Note you should always want to use ``requirements-dev`` instead of
``requirements`` (as a developer that it).


If you want to verify you code against ``flake8`` (and you SHOULD) run::

  tox -e check

It will output a results report in ``output/code_analysis/flake8``.


To build the documentation::

  tox -e docs

