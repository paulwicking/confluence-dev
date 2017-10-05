import confluence
try:
    from unittest.mock import patch
    import unittest.mock as mock
except ImportError:
    from mock import patch
    import mock
import pytest
import requests


@pytest.fixture()
def mock_conf():
    return mock.Mock(spec=confluence.Confluence)


@patch('confluence.Confluence.connection_valid')
def test_confluence_init_method(mock_connection_valid):
    """Tests Confluence.__init__().

    This test uses a mock for the connection_valid() method in the class, as this is called by __init__() and requires
    network access.

    :param mock_connection_valid: Intercepted by unittest.mock.patch and replaces connection_valid() during test..
    """
    mock_connection_valid.return_value = True
    conf = confluence.Confluence(profile='general')

    assert conf is not None


def test_confluence_init_method_ok():
    """Tests Confluence.__init__().

    This test mocks the session created with requests.Session and asserts that the connection check passes.
    """

    def mock_get_ok(mock_self, mock_response):
        """

        :param foo:
        :param bar:
        :return:
        """
        return_object = mock.Mock()
        return_object.ok = True
        return return_object

    with mock.patch.object(requests.Session, 'get', new=mock_get_ok):
        conf = confluence.Confluence(profile='general')
        assert conf.connection is not None
        assert conf.connection_valid()


def test_confluence_init_method_fails():

    def mock_get_fail(foo, bar):
        return_object = mock.Mock()
        return_object.ok = False
        return return_object

    with mock.patch.object(requests.Session, 'get', new=mock_get_fail):
        conf = confluence.Confluence(profile='general')
        assert not conf.connection_valid()
        assert conf.connection is None


def test_connection_valid_raises_exceptions():
    """Test that connection_valid() calls requests.raise_for_status.

    This test mocks the session created with requests.Session and asserts that the connection check fails.
    """
    with pytest.raises(requests.exceptions.RequestException):
        conf = confluence.Confluence()


def test_get_blog_entry_with_clean_results():
    pass
#     expected_response = {
#         'author': 'wowsuchnamaste',
#         'content': '<p><ac:structured-macro ac:name="loremipsum" ac:schema-version="1" \
#         ac:macro-id="d63b8ee8-b840-4679-abd1-4008de8d3adf" /></p><p><br /></p><p>version 2</p>',
#         'id': '1179661',
#         'permissions': '0',
#         'publishDate': '< DateTime 20170321T10:31:16 at 0x7fe1eff45198 >',
#         'space': '~wowsuchnamaste',
#         'title': 'This is my first blog post.',
#         'url': 'https://confluence/pages/viewpage.action?pageId=1179661',
#         'version': '2'}
#
#     actual_response = 'some string to change'
#
#     assert expected_response in actual_response


@patch('xmlrpc.client.ServerProxy')
def test_pending_deprecation_warnings(mock_server):
    """Test that calling XMLRPC methods issue pending deprecation warnings.

    When XML-RPC based methods are called, the pending_deprecation wrapper function issues a warning.

    :param mock_server: Intercepted by unittest.mock.patch and replaces xmlrpclib during test.
    """
    mock_server.confluence2.getSpaces.return_value = True
    conf = confluence.Confluence()
    with warnings.catch_warnings(record=True) as warn:
        warnings.simplefilter('always')
        conf.getSpaces()

        assert issubclass(warn[-1].category, PendingDeprecationWarning)
        assert "use the Atlassian REST API in future versions" in str(warn[-1].message)


def test_check_response_returns_false_on_invalid_response(mock_conf):
    """"Tests that invalid response checks return False.

    :param mock_conf: pytest decorator that returns a Mock Confluence object.
    """
    # call_that_causes_404 = conf.connection.get(conf.base_url +
    #                                            'space/content?type=page&spaceKey=ds')
    # call_that_returns_empty_results_list = conf.get_page_id('ds', 'another page')
    #
    # assert conf.check_response(call_that_causes_404) is False
    # assert conf.check_response(call_that_returns_empty_results_list) is False
    pass


def test_check_reponse():
    def mock_get_ok(mock_self, mock_response):
        """Mock method to pass as the mock.patch.object in this test.

        :param mock_self: Mock the self parameter of connection_valid().
        :param mock_response: Mock the response parameter of connection_valid().
        :return: Mock object with property ok = True.
        """
        return_object = mock.Mock()
        return_object.ok = True
        return return_object

    with mock.patch.object(requests.Session, 'get', new=mock_get_ok):
        conf = confluence.Confluence()
        response_is_none = None
        mock_response = mock.Mock()

        assert conf.check_response(response_is_none) is False


def test_check_response_returns_true_on_valid_response(mock_conf):
    """

    :param mock_conf: pytest decorator that returns a Mock Confluence object.
    """
    # call_that_succeeds = conf.connection.get(conf.base_url +
    #                                          'content?type=page&spaceKey=ds')
    # assert conf.check_response(call_that_succeeds) is True
    pass
