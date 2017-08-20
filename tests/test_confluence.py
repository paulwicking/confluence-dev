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


def test_invalid_connections_raise_exception():
    """Tests that invalid connections raise ConnectionError exception."""
    #  TODO write this test.
    pass


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


def test_pending_deprecation_warnings():
    with warnings.catch_warnings(record=True) as warn:
        warnings.simplefilter('always')
        conf = confluence.Confluence(profile='pycontribs-test')
        conf.getSpaces()

        assert issubclass(warn[-1].category, PendingDeprecationWarning)
        assert "use the Atlassian REST API in future versions" in str(warn[-1].message)

    conf.connection.close()


def test_get_page_id():
    """Tests that page id is returned as expected."""
    conf = confluence.Confluence(profile='pycontribs-test')
    expected_response = 425986
    response = conf.get_page_id('ds', 'Tell people what you think in a comment (step 8 of 9)')

    expected_blog_response = 60325915
    blog_response = conf.get_page_id('wst', 'The Camelot Song', content_type='blogpost')

    assert isinstance(response, int)
    assert response == expected_response
    assert response != 42

    assert isinstance(blog_response, int)
    assert blog_response == expected_blog_response
    assert blog_response != 42

    conf.connection.close()


def test_get_spaces_with_full_json_response():
    """Test retrieval of a JSON formatted dict of spaces from the server."""
    conf = confluence.Confluence(profile='pycontribs-test')
    result = conf.get_spaces(full=True)

    assert isinstance(result, dict)
    assert 'Demonstration Space' in result['results'][0]['name']
    assert 'elderberries' not in result['results'][0]['name']

    conf.connection.close()


def test_get_spaces_with_pretty_response():
    """Test retrieval of a list of spaces from the server."""
    conf = confluence.Confluence(profile='pycontribs-test')
    result = conf.get_spaces()

    assert isinstance(result, list)
    assert 'Demonstration Space' in result[0]['name']
    assert 'elderberries' not in result[0]['name']

    conf.connection.close()


def test_get_blog_entry_with_full_json_response():
    conf = confluence.Confluence(profile='pycontribs-test')
    result = conf.get_blog_entry('wst', 'The Camelot Song', post_date='2017-08-19', full=True)

    assert 'The Camelot Song' in result['results'][0]['title']
    assert 'blogpost' in result['results'][0]['type']
    assert 'Clark Gable' in result['results'][0]['body']['view']['value']
    assert 'elderberries' not in result['results'][0]['title']

    conf.connection.close()


def test_get_page_with_full_json_response():
    """Test that we can retrieve one specific page."""
    conf = confluence.Confluence(profile='pycontribs-test')
    result = conf.get_page('ds', 'Get serious with a table (step 5 of 9)', full=True)

    assert 'page' in result['results'][0]['type']
    assert 'Get serious with a table' in result['results'][0]['title']
    assert 'elderberries' not in result['results'][0]['body']['storage']['value']
    assert 'Your table should look like this:' in result['results'][0]['body']['storage']['value']

    conf.connection.close()


def test_get_page_with_pretty_response():
    """Test that we can retrieve one specific page as a dict."""
    conf = confluence.Confluence(profile='pycontribs-test')
    result = conf.get_page('ds', 'Get serious with a table (step 5 of 9)')

    assert isinstance(result, dict)

    assert 'title' in result.keys()
    assert 'Get serious with a table' in result['title']
    assert 'elderberries' not in result['content']
    assert 'Your table should look like this:' in result['content']

    conf.connection.close()


def test_get_pages_with_full_json_response():
    """Test retrieval of a JSON formatted dict of spaces from the server."""
    conf = confluence.Confluence(profile='pycontribs-test')
    result = conf.get_pages('ds', full=True)

    assert isinstance(result, dict)
    assert "Let's edit this page (step 3 of 9)" in result['results'][0]['title']
    assert 'elderberries' not in result['results'][0]['title']

    conf.connection.close()


def test_get_pages_with_pretty_response():
    """Test that we get a list with the pages in a space from the server."""
    conf = confluence.Confluence(profile='pycontribs-test')
    result = conf.get_pages('ds')

    assert isinstance(result, list)
    assert len(result) == 10

    conf.connection.close()
