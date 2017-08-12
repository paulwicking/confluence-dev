# import base64
# import json
import logging
import requests
# from requests import Request, Session
from requests.auth import HTTPBasicAuth

# Debug imports only
# import importlib  # for importlib.reload()

log = logging.getLogger(__name__)


class Confluence(object):
    def __init__(self, url, user, password):
        """Set the defaults for the object."""
        self.url = url  # 'http://localhost:8090'
        self._user = user  # 'myusername'
        self._password = password  # 'mypassword'

        # Set the base URL for REST calls.
        self.base_url = url + '/rest/api/'

        # Create a request session.
        self.connection = requests.Session()
        self.connection.auth = HTTPBasicAuth(self._user, self._password)

        if not self.connection_valid():
            log.critical("Connection is None.")

        log.debug("")

    def connection_valid(self):
        """Checks if a connection to the Confluence server can be established.

        :rtype: Boolean
        """
        try:
            result = self.connection.get(self.url)
        except ConnectionError:
            log.exception("Connection Error: Check username, password and url.")
            raise ConnectionError("Fatal error. Could not establish a valid connection.")

        if not result.ok:
            self.connection = None
        return self.connection is not None

    def get_spaces(self):
        """Returns all spaces on the server.

        :rtype: TODO @wowsuchnamaste insert rtype
        """

        request = self.base_url + "space"
        response = self.connection.get(request)
        if not response.ok:
            response = False

        return response

    def get_pages(self, space):
        """Get all pages in a space.

        :param space: The space name
        :type  space: ``str``

        :rtype: ``list``
        :return: a list of pages in a space
        """
        request = self.base_url + "content?spaceKey=" + space
        response = self.connection.get(request)
        return response

    def get_page(self, page, space):
        """Returns a page as dict.

        :parameter page: string containing the name of the page.
        :parameter space: string containing the space key.

        :returns The page as a dict.
        """
        # request = self.baseurl + 'content?title=' + page + '&spaceKey=' + space
        # print(f'DEBUG: {request}')
        # page = requests.get(request, self._auth)
        pass

    def getPageId(self, page, space):
        """Retuns the numeric id of a confluence page.

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :rtype: ``int``
        :return: Page numeric id
        """

        # request = self.base_url + f"content?spaceKey={space}?page={page}"

    def attach_file(self, page, space, files):
        """Attach a file to a page.

        :parameter page: The page name
        :type  page: ``str``

        :parameter space: The space name
        :type  space: ``str``

        :parameter files: The files to upload
        :type  files: ``dict`` where `key` is filename and `value` is the comment.
        """
        # def attach_file(server, token, space, title, files):      #  duplicate function definition
        pass

    def remove_all_attachments(self, server, token, space, title):
        pass

    def write_page(self, server, token, space, title, content, parent=None):
        pass

    def get_blog_entries(self, space):
        """Get all blog entries in the specified space.

        :parameter space: ``str`` Space name.
        """
        pass

    def get_blog_entry(self, page_id):
        """Get a specific blog page.

        :parameter page_id: ``int`` The page ID.
        """
        pass

    def store_blog_entry(self, entry):
        """Store or update blog content.
        (The BlogEntry given as an argument should have space, title and content fields at a minimum.)

        :param entry: Blog entry
        :type  entry: ``str``

        :rtype: ``bool``
        :return: `true` if succeeded
        """
        pass

    def add_label_by_name(self, label_name, object_id):
        """Adds label(s) to the object.

        :param object_id: Such as pageId
        :type object_id: ``str``

        :param label_name: Tag Name
        :type label_name: ``str``


        :param objectId:
        :type  objectId:

        :rtype: ``bool``
        :return: True if succeeded
        """
        pass

    def movePage(self, sourcePageIds, targetPageId, space, position='append'):
        """
        Moves sourcePage to be a child of targetPage by default.  Modify 'position' to either 'above' or 'below'
        to make sourcePage a sibling of targetPage, and place it either directly above or directly below targetPage
        in the hierarchy, respectively.

        :param sourcePageIds: List of pages to be moved to targetPageId
        :param targetPageId: Name or PageID of new parent or target sibling
        :param position: Defaults to move page to be child of targetPageId \
                         Setting 'above' or 'below' instead sets sourcePageId \
                         to be a sibling of targetPageId of targetPageId instead
        """
        pass

    def storePageContent(self, page, space, content, convert_wiki=True, parent_page=None):
        """
        Modifies the content of a Confluence page.

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :param content: The page content (wiki markup or rich text)
        :type  content: ``str``

        :param convert_wiki: Convert content as wiki markup before updating
        :type  convert_wiki: ``bool``

        :param parent_page: The parent page name (optional)
        :type  parent_page: ``str``

        :rtype: ``bool``
        :return: `True` if succeeded
        """
        pass

    def render_content(self, space, page, a='', b={'style': 'clean'}):
        """Obtains the HTML content of a wiki page.

        :param b:
        :param a:
        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :return: string: HTML content
        """
        pass

    def convertWikiToStorageFormat(self, markup):
        """Converts a wiki text to it's XML/HTML format. Useful if you prefer to generate pages using wiki syntax instead of XML.

        Still, remember that once you cannot retrieve the original wiki text, as confluence is not storing it anymore. \
        Due to this wiki syntax is usefull only for computer generated pages.

        Warning: this works only with Conflucence 4.0 or newer, on older versions it will raise an error.

        :param markup: The wiki markup
        :type  markup: ``str``

        :rtype: ``str``
        :return: the text to store (HTML)
        """
        pass

    def getPagesWithErrors(self, stdout=True, caching=True):
        """Get pages with formatting errors."""
        pass
