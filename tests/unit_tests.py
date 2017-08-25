# from confluence import Confluence
import confluence
from unittest.mock import MagicMock, patch
import unittest.mock
import pytest


def setup_module(module):
    print('setup_module')


# @pytest.fixture
# def mock_conf():
#     return unittest.mock.Mock(spec=Confluence)


def test_connection_valid():
    # CONF = unittest.mock.Mock(return_value=mock_conf)
    # monkeypatch.setattr('confluence.Confluence', CONF)
    # conf = CONF
    # mock_conf.connection = 'object'
    # assert conf.valid_connection() == 'object'
    # with mock.patch('confluence.test_valid_connection') as mock_requests:
    #     test_connection_valid()
    #
    #     mock_requests.assert_called_once_with('http://localhost')
    with patch('confluence.Confluence') as mock:
        instance = mock.return_value
        instance.method.return_value = 'the result'
        result = confluence.Confluence()
        assert result == 'the result'


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
#         'url': 'https://wowsu.ch/confluence/pages/viewpage.action?pageId=1179661',
#         'version': '2'}
#
#     actual_response = 'some string to change'
#
#     assert expected_response in actual_response


def teardown_module(module):
    print('teardown_module')
