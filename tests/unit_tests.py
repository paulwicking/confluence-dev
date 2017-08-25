# from confluence import Confluence
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
    mock_confl = mock.Mock(spec=confluence.Confluence)
    return mock_confl

#
# def test_connection_valid():
#     # CONF = unittest.mock.Mock(return_value=mock_conf)
#     # monkeypatch.setattr('confluence.Confluence', CONF)
#     # conf = CONF
#     # mock_conf.connection = 'object'
#     # assert conf.valid_connection() == 'object'
#     # with mock.patch('confluence.test_valid_connection') as mock_requests:
#     #     test_connection_valid()
#     #
#     #     mock_requests.assert_called_once_with('http://localhost')
#     with patch('confluence.Confluence') as mock:
#         instance = mock.return_value
#         instance.method.return_value = 'the result'
#         result = confluence.Confluence()
#         assert result is not None


@patch('confluence.Confluence.connection_valid')
def test_confluence_init_method(mock_connection_valid):
    mock_connection_valid.return_value = True
    conf = confluence.Confluence(profile='pycontribs-test')

    assert conf is not None


def test_confluence_init_method_ok():

    def mock_get_ok(foo, bar):
        return_object = mock.Mock()
        return_object.ok = True
        return return_object

    with mock.patch.object(requests.Session, 'get', new=mock_get_ok):
        # mock_connection_valid.return_value = None
        conf = confluence.Confluence(profile='pycontribs-test')
        assert conf.connection is not None
        assert conf.connection_valid()


def test_confluence_init_method_fails():

    def mock_get_fail(foo, bar):
        return_object = mock.Mock()
        return_object.ok = False
        return return_object

    with mock.patch.object(requests.Session, 'get', new=mock_get_fail):
        conf = confluence.Confluence(profile='pycontribs-test')
        assert not conf.connection_valid()
        assert conf.connection is None


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


def test_just_a_try(mock_conf):

    conf = mock_conf()
    print(type(conf.connection_valid))
