import pytest
from confluence import confluence2


@pytest.mark.xfail
def test_valid_connection():
    """Checks that valid_connection() works and that it passes for the right reason."""
    conf = confluence2.Confluence(url='http://localhost:1990/confluence', username='admin', password='admin')
    url_to_get = conf.base_url + 'content'
    response = conf.connection.get(url_to_get)

    assert conf.connection_valid() is True
    assert isinstance(url_to_get, object)
    assert response.json()['_links']['self'] == url_to_get


def test_invalid_connections_raise_exception():
    """Tests that invalid connections raise ConnectionError exception."""
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
