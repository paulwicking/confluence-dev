# import pytest
from confluence import confluence
import warnings


def test_valid_connection():
    """Checks that valid_connection() works and that it passes for the right reason."""
    conf = confluence.Confluence(profile='general')
    url_to_get = conf.base_url + 'content'
    response = conf.connection.get(url_to_get)

    assert conf.connection_valid() is True
    assert isinstance(url_to_get, object)
    assert response.json()['_links']['self'] == url_to_get

    conf.connection.close()


def test_invalid_connections_raise_exception():
    """Tests that invalid connections raise ConnectionError exception."""
    pass


# @pytest.mark.xfail
# def test_connection_to_atlassian_sdk():
#     """Test that we can connect to the Atlassian SDK during test"""
#     conf = confluence.Confluence(profile='atlassian-sdk')
#     result = conf.getSpaces()
#
#     assert isinstance(conf, object)
#     assert not isinstance(conf, int)
#     assert 'key' in result[0]
#     assert result[0]['name'] == 'Demonstration Space'
#     assert 'pink fluffy unicorns' not in result[0]
#
#     conf.connection.close()


def test_pending_deprecation_warnings():
    with warnings.catch_warnings(record=True) as warn:
        warnings.simplefilter('always')
        conf = confluence.Confluence(profile='general')
        conf.getSpaces()

        assert issubclass(warn[-1].category, PendingDeprecationWarning)
        assert "use the Atlassian REST API in future versions" in str(warn[-1].message)

    conf.connection.close()


def test_get_spaces():
    """Test to make sure we can get a list of spaces from the server."""
    conf = confluence.Confluence(profile='general')
    result = conf.get_spaces()

    assert 'Demonstration Space' in result['results'][0]['name']
    assert 'elderberries' not in result['results'][0]['name']

    conf.connection.close()


def test_get_pages():
    """Test that we get the pages in a space from the server."""
    pass


def test_get_page():
    """Test that we can retrieve one specific page."""
    pass
