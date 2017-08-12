import pytest
from confluence import confluence2


@pytest.mark.cannot_fail
def test_tests():
    """A test test, testing we're not failing tests for no reason."""
    pass


def test_get_spaces():
    """Test to make sure we can get a list of spaces from the server."""
    pass


def test_get_pages():
    """Test that we get the pages in a space from the server."""
    pass


def test_get_page():
    """Test that we can retrieve one specific page."""
    pass
