# from confluence import Confluence
# import unittest.mock as mock
#
#
# def test_connection_valid():
#     with mock.patch('confluence.requests.get') as mock_requests:
#         test_connection_valid()
#
#         mock_requests.assert_called_once_with('http://localhost')
#
#
# def test_get_blog_entry_with_clean_results():
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
