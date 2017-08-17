#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from requests.auth import HTTPBasicAuth
# from functools import partial

# import copy
import functools
# import json
import logging
import os
# import re
import requests
import socket
# import ssl
import sys
import warnings

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser


log = logging.getLogger(__name__)


def _pending_deprecation(old_function, replacement=None, reason=None):
    """Decorator for soon-to-be deprecated functions. Produces warning.

    :param old_function: The function that will be deprecated.
    :type  old_function: ``function``

    :param replacement: Optional replacement function.
    :type  replacement: ``function``

    :param reason: Optional string describing the reason.
    :type  reason: ``str``
    """

    @functools.wraps(old_function)
    def new_function(*args, **kwargs):
        warnings.simplefilter('always', PendingDeprecationWarning)
        warnings.warn('{} will be deprecated in the future.'.format(old_function.__name__),
                      category=PendingDeprecationWarning, stacklevel=2)
        if replacement:
            warnings.warn('Use {} instead'.format(replacement.__name__),
                          category=PendingDeprecationWarning, stacklevel=2)
        if reason:
            warnings.warn('Reason: {}'.format(str(reason)),
                          category=PendingDeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', PendingDeprecationWarning)

        return old_function(*args, **kwargs)

    return new_function
# pending_deprecation = partial(_pending_deprecation,


class Confluence(object):
    def __init__(self, url, username, password):
        """Set the defaults for the object."""
        self._url = url  # 'http://localhost:8090'
        self._user = username  # 'myusername'
        self._password = password  # 'mypassword'

        # Set the base URL for REST calls.
        self.base_url = url + '/rest/api/'

        # Create a request session.
        self.connection = requests.Session()
        self.connection.auth = HTTPBasicAuth(self._user, self._password)

        if not self.connection_valid():
            log.critical('Connection is None.')

        log.debug("Instantiated object.")

    def connection_valid(self):
        """Checks if a connection to the Confluence server can be established.

        :rtype: Boolean
        """
        try:
            result = self.connection.get(self.base_url + 'content')
        except requests.ConnectionError as err:
            log.exception('Connection Error: Check username, password and url.')
            print(err)
            raise err

        if not result.ok:
            self.connection = None
        return self.connection is not None

    def get_spaces(self):
        """Returns all spaces on the server.

        :rtype: TODO @wowsuchnamaste insert rtype
        """

        request = self.base_url + 'space'
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


class ConfluenceOld(object):

    DEFAULT_OPTIONS = {
        "server": "http://localhost:8090",
        "verify": True
    }

    def __init__(self, profile=None, url="http://localhost:8090/", username=None, password=None, appid=None, debug=False):
        """
        Returns a Confluence object by loading the connection details from the `config.ini` file.

        :param profile: The name of the section from config.ini file that stores server config url/username/password
        :type  profile: ``str``

        :param url: URL of the Confluence server
        :type  url: ``str``

        :param username: username to use for authentication
        :type  username: ``str``

        :param password: password to use for authentication
        :type  password: ``str``

        :return: Confluence -- an instance to a Confluence object.
        :raises: EnvironmentError

        Usage:

            >>> from confluence import Confluence
            >>>
            >>> conf = Confluence(profile='confluence')
            >>> conf.storePageContent("test","test","hello world!")

        Also create a `config.ini` like this and put it in current directory, user home directory or PYTHONPATH.

        .. code-block:: none

            [confluence]
            url=https://confluence.atlassian.com
            # only the `url` is mandatory
            user=...
            pass=...

        """
        def findfile(path):
            """
            Find the file named path in the sys.path.
            Returns the full path name if found, None if not found
            """
            paths = [os.getcwd(), '.', os.path.expanduser('~')]
            paths.extend(sys.path)
            for dirname in paths:
                possible = os.path.abspath(os.path.join(dirname, path))
                if os.path.isfile(possible):
                    return possible
            return None

        config = ConfigParser.SafeConfigParser(defaults={'user': username, 'pass': password, 'appid': appid})

        config_file = findfile('config.ini')
        if debug:
            print(config_file)

        if not profile:
            if config_file:
                config.read(config_file)
                try:
                    profile = config.get('general', 'default-confluence-profile')
                except ConfigParser.NoOptionError:
                    pass

        if profile:
            if config_file:
                config.read(config_file)
                url = config.get(profile, 'url')
                username = config.get(profile, 'user')
                password = config.get(profile, 'pass')
                appid = config.get(profile, 'appid')
            else:
                raise EnvironmentError("%s was not able to locate the config.ini file in current directory, user home directory or PYTHONPATH." % __name__)

        options = Confluence.DEFAULT_OPTIONS
        options['server'] = url
        options['username'] = username
        options['password'] = password

        socket.setdefaulttimeout(120)  # without this there is no timeout, and this may block the requests
        # 60 - getPages() timeout one with this !
        # self._server = xmlrpclib.ServerProxy(
        #     options['server'] +
        #     '/rpc/xmlrpc', allow_none=True)  # using Server or ServerProxy ?

        # TODO: get rid of this split and just set self.server, self.token
        # self._token = self._server.confluence1.login(username, password)
        # try:
        #    self._token2 = self._server.confluence2.login(username, password)
        # except xmlrpclib.Error:
        #     self._token2 = None

    def getPage(self, page, space):
        """
        Returns a page object as a dictionary.

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :return: dictionary. result['content'] contains the body of the page.
        """
        pass

    def getAttachments(self, page, space):
        """
        Returns a attachments as a dictionary.

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :return: dictionary. result['content'] contains the body of the page.
        """
        pass

    def getAttachedFile(self, page, space, fileName):
        """
        Returns a attachment data as byte[].

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :param fileName: The attached file name
        :type  fileName: ``str``
        """
        pass

    def attachFile(self, page, space, files):
        """
        Attach (upload) a file to a page

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :param files: The files to upload
        :type  files: ``dict`` where `key` is filename and `value` is the comment.
        """
        pass

    def getBlogEntries(self, space):
        """
        Returns a page object as a Vector.

        :param space: The space name
        :type  space: ``str``
        """
        pass

    def getBlogEntry(self, pageId):
        """
        Returns a blog page as a BlogEntry object.

        :param pageId:
        """
        pass

    def storeBlogEntry(self, entry):
        """
        Store or update blog content.
        (The BlogEntry given as an argument should have space, title and content fields at a minimum.)

        :param entry: Blog entry
        :type  entry: ``str``

        :rtype: ``bool``
        :return: `true` if succeeded
        """
        pass

    def addLabelByName(self, labelName, objectId):
        """
        Adds label(s) to the object.

        :param labelName: Tag Name
        :type  labelName: ``str``

        :param objectId: Such as pageId
        :type  objectId: ``str``

        :rtype: ``bool``
        :return: True if succeeded
        """
        pass

    def getPageId(self, page, space):
        """
        Retuns the numeric id of a confluence page.

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :rtype: ``int``
        :return: Page numeric id
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

    def renderContent(self, space, page, a='', b={'style': 'clean'}):
        """
        Obtains the HTML content of a wiki page.

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :return: string: HTML content
        """

        pass

    def convertWikiToStorageFormat(self, markup):
        """
        Converts a wiki text to it's XML/HTML format. Useful if you prefer to generate pages using wiki syntax instead of XML.

        Still, remember that once you cannot retrieve the original wiki text, as confluence is not storing it anymore. \
        Due to this wiki syntax is usefull only for computer generated pages.

        Warning: this works only with Conflucence 4.0 or newer, on older versions it will raise an error.

        :param markup: The wiki markup
        :type  markup: ``str``

        :rtype: ``str``
        :return: the text to store (HTML)
        """
        pass

    def getSpaces(self):
        pass

    def getPages(self, space):
        """
        Get pages in a space

        :param space: The space name
        :type  space: ``str``

        :rtype: ``list``
        :return: a list of pages in a space
        """
        pass

    def getPagesWithErrors(self, stdout=True, caching=True):
        """
        Get pages with formatting errors
        """
        pass


# TODO: replace all of these with object methods. Leaving for backwards compatibility for now
def attach_file(server, token, space, title, files):
    pass


def remove_all_attachments(server, token, space, title):
    pass


def write_page(server, token, space, title, content, parent=None):
    pass
