import pytest
from confluence import confluence
import warnings


@pytest.fixture(scope='module')
def conf():
    test_conf = confluence.Confluence(profile='pycontribs-test')
    yield test_conf

    # Teardown
    test_conf.connection.close()


def test_valid_connection(conf):
    """Checks that valid_connection() works and that it passes for the right reason."""
    # conf = confluence.Confluence(profile='pycontribs-test')
    url_to_get = conf.rest_url + 'content'
    response = conf.connection.get(url_to_get)

    assert conf.connection_valid() is True
    assert isinstance(url_to_get, object)
    assert response.json()['_links']['self'] == url_to_get


def test_check_response_is_404_on_invalid_request(conf):
    call_that_causes_404 = conf.connection.get(conf.rest_url +
                                               'space/content?type=page&spaceKey=ds')
    assert conf.check_response(call_that_causes_404) is False


def test_check_response_with_empty_results_list_is_false(conf):
    call_that_returns_empty_results_list = conf.get_page_id('ds', 'another page')
    assert conf.check_response(call_that_returns_empty_results_list) is False


def test_check_response_with_successful_request_is_true(conf):
    """"Tests that valid responses return True, invalid responses False."""
    call_that_succeeds = conf.connection.get(conf.rest_url +
                                             'content?type=page&spaceKey=ds')
    assert conf.check_response(call_that_succeeds) is True


def test_pending_deprecation_warnings(conf):
    with warnings.catch_warnings(record=True) as warn:
        warnings.simplefilter('always')
        conf.getSpaces()

        assert issubclass(warn[-1].category, PendingDeprecationWarning)
        assert "use the Atlassian REST API in future versions" in str(warn[-1].message)


def test_get_page_id(conf):
    """Tests that page id is returned as expected."""
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


def test_get_spaces_with_full_json_response(conf):
    """Test retrieval of a JSON formatted dict of spaces from the server."""
    result = conf.get_spaces(full=True)

    assert isinstance(result, dict)
    assert 'Demonstration Space' in result['results'][0]['name']
    assert 'elderberries' not in result['results'][0]['name']


def test_get_spaces_with_pretty_response(conf):
    """Test retrieval of a list of spaces from the server."""
    result = conf.get_spaces()

    assert isinstance(result, list)
    assert 'Demonstration Space' in result[0]['name']
    assert 'elderberries' not in result[0]['name']


def test_get_blog_entry_with_full_json_response(conf):
    result = conf.get_blog_entry('wst', 'The Camelot Song', post_date='2017-08-19', full=True)

    assert 'The Camelot Song' in result['results'][0]['title']
    assert 'blogpost' in result['results'][0]['type']
    assert 'Clark Gable' in result['results'][0]['body']['view']['value']
    assert 'elderberries' not in result['results'][0]['title']


def test_get_page_with_full_json_response(conf):
    """Test that we can retrieve one specific page."""
    result = conf.get_page('ds', 'Get serious with a table (step 5 of 9)', full=True)

    assert 'page' in result['results'][0]['type']
    assert 'Get serious with a table' in result['results'][0]['title']
    assert 'elderberries' not in result['results'][0]['body']['storage']['value']
    assert 'Your table should look like this:' in result['results'][0]['body']['storage']['value']


def test_get_page_with_pretty_response(conf):
    """Test that we can retrieve one specific page as a dict."""
    result = conf.get_page('ds', 'Get serious with a table (step 5 of 9)')

    assert isinstance(result, dict)

    assert 'title' in result.keys()
    assert 'Get serious with a table' in result['title']
    assert 'elderberries' not in result['content']
    assert 'Your table should look like this:' in result['content']


def test_get_pages_with_full_json_response(conf):
    """Test retrieval of a JSON formatted dict of spaces from the server."""
    result = conf.get_pages('ds', full=True)

    assert isinstance(result, dict)
    assert "Let's edit this page (step 3 of 9)" in result['results'][0]['title']
    assert 'elderberries' not in result['results'][0]['title']


def test_get_pages_with_pretty_response(conf):
    """Test that we get a list with the pages in a space from the server."""
    result = conf.get_pages('ds')

    assert isinstance(result, list)
    assert len(result) == 10
