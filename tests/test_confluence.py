# import pytest
from confluence import confluence
import warnings


def test_valid_connection():
    """Checks that valid_connection() works and that it passes for the right reason."""
    conf = confluence.Confluence(profile='pycontribs-test')
    url_to_get = conf.base_url + 'content'
    response = conf.connection.get(url_to_get)

    assert conf.connection_valid() is True
    assert isinstance(url_to_get, object)
    assert response.json()['_links']['self'] == url_to_get

    conf.connection.close()


def test_check_response():
    """"Tests that valid responses return True, invalid responses False."""
    conf = confluence.Confluence(profile='pycontribs-test')
    call_that_causes_404 = conf.connection.get(conf.base_url +
                                               'space/content?type=page&spaceKey=ds')
    call_that_returns_empty_results_list = conf.get_page_id('ds', 'another page')
    call_that_succeeds = conf.connection.get(conf.base_url +
                                             'content?type=page&spaceKey=ds')

    assert conf.check_response(call_that_causes_404) is False
    assert conf.check_response(call_that_returns_empty_results_list) is False
    assert conf.check_response(call_that_succeeds) is True

    conf.connection.close()


def test_get_page_id():
    """Tests that page id is returned as expected."""
    conf = confluence.Confluence(profile='pycontribs-test')
    expected_response = 425986
    response = conf.get_page_id('ds', 'Tell people what you think in a comment (step 8 of 9)')

    assert response == expected_response
    assert response != 42
    assert isinstance(response, int)

    conf.connection.close()


def test_pending_deprecation_warnings():
    with warnings.catch_warnings(record=True) as warn:
        warnings.simplefilter('always')
        conf = confluence.Confluence(profile='pycontribs-test')
        conf.getSpaces()

        assert issubclass(warn[-1].category, PendingDeprecationWarning)
        assert "use the Atlassian REST API in future versions" in str(warn[-1].message)

    conf.connection.close()


def test_get_spaces():
    """Test to make sure we can get a list of spaces from the server."""
    conf = confluence.Confluence(profile='pycontribs-test')
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


def test_invalid_connections_raise_exception():
    """Tests that invalid connections raise ConnectionError exception."""
    pass
