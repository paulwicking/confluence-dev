import pytest
from confluence import confluence
import warnings


def test_valid_connection():
    """Checks that valid_connection() works and that it passes for the right reason."""
    conf = confluence.Confluence(url='http://localhost:1990/confluence', username='admin', password='admin')
    url_to_get = conf._server + 'content'
    response = conf.connection.get(url_to_get)

    assert conf.connection_valid() is True
    assert isinstance(url_to_get, object)
    assert response.json()['_links']['self'] == url_to_get


def test_invalid_connections_raise_exception():
    """Tests that invalid connections raise ConnectionError exception."""
    pass


def test_connection_to_atlassian_sdk():
    """Test that we can connect to the Atlassian SDK during test"""
    conf = confluence.Confluence(url='http://localhost:1990/confluence', username='admin', password='admin')
    result = conf.getSpaces()
    assert isinstance(conf, object)
    assert not isinstance(conf, int)
    assert 'key' in result[0]
    assert result[0]['name'] == 'Demonstration Space'
    assert 'pink fluffy unicorns' not in result[0]


@pytest.mark.xfail
def test_pending_deprecation_warnings():
    with warnings.catch_warnings(record=True) as warn:
        warnings.simplefilter('always')
        conf = confluence.Confluence(url='http://127.0.0.1:1990/confluence', username='admin', password='admin')
        conf.getSpaces()

        assert len(warn) == 1
        assert issubclass(warn[-1].category, PendingDeprecationWarning)
        assert "deprecated" in str(warn[-1].message)


def test_get_spaces():
    """Test to make sure we can get a list of spaces from the server."""
    pass


def test_get_pages():
    """Test that we get the pages in a space from the server."""
    pass


def test_get_page():
    """Test that we can retrieve one specific page."""
    pass
