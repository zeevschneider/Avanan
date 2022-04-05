"""Information about what this test-suite includes."""


def test_true_is_not_false():
    """All tests shouls have docstring that specifies what the test do. This
    information is being extracted and later showing in the results report.
    """
    state = True
    assert state is not False
