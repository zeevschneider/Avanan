"""Pytest Configuration."""

import logging
import pytest
from py.xml import html


def pytest_addoption(parser):
    """Add CLI options to py.test. """
    desc = "File where detailed log will be stored"
    default_log_file = "tests/logs/tests.log"
    dest = "logging_file"
    group = parser.getgroup("logging", "Logging Configuration")
    group.addoption(
        "--logging-file", dest=dest, default=default_log_file, help=desc,
    )
    parser.addini(dest, desc, default=default_log_file)
#
#
# def pytest_configure(config):
#     """Add the formatter to logging. """
#     log_file = config.getini("logging_file") or config.getvalue("logging_file")
#     logging.root.addHandler(logging.FileHandler(log_file))


def pytest_itemcollected(item):
    """Monkey patching pytest to collect function description rather than the
    name for the report.
    """
    node = item.obj
    doc = node.__doc__.strip()

    if doc:
        doc = doc.split("\n", 1)[0]
    else:
        doc = node.__name__

    # pylint: disable=protected-access
    item._nodeid = " ".join((item.nodeid, doc))


@pytest.mark.optionalhook
# pylint: disable=invalid-name
def pytest_html_results_table_header(cells):
    """Hook that is being called by 'pytest-html' when rendering the headers
    of the report table (which eventually adds a row with test's docstring).
    """
    cells[1] = html.th("Description")
    cells.insert(2, html.th("Location"))


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    """Hook that is called by ``pytest-html`` when rendering the body of the
    report table (which eventually adds a row with test's docstring).
    """
    desc, loc = report.nodeid.split(" ", 1)
    cells.insert(2, html.td(desc))
    cells[1] = html.td(loc)
