#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from requests.auth import HTTPBasicAuth

import copy
import functools
import json
import logging
import os
import re
import requests
import socket
import ssl
import sys
import warnings

try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """Returns a new instance of the NullHandler class."""
        def emit(self, record):
            """This method does nothing."""
            pass

logging.getLogger('confluence').addHandler(NullHandler())


def deprecate_xmlrpc_notification(func):
    """Decorator for xmlrpc deprecation warnings."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        # warnings.simplefilter('always', PendingDeprecationWarning)  # Un-comment this line to always display warnings.
        warnings.warn(
            "{} will be rewritten to use the Atlassian REST API in future versions.\n"
            "This change will introduce changes in the module method responses.".format(func.__name__),
            category=PendingDeprecationWarning,
            stacklevel=2)
        warnings.simplefilter('default', PendingDeprecationWarning)
        return func(*args, **kwargs)
    return new_func


# TODO: replace all of these with object methods. Leaving for backwards compatibility for now
@deprecate_xmlrpc_notification
def attach_file(server, token, space, title, files):
    existing_page = server.confluence1.getPage(token, space, title)

    for filename in files.keys():
        try:
            server.confluence1.removeAttachment(token, existing_page["id"], filename)
        except Exception as e:
            logging.exception("Skipping %s exception in removeAttachment" % e)
        content_types = {
            "gif": "image/gif",
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
        }
        extension = os.path.spl(filename)[1]
        ty = content_types.get(extension, "application/binary")
        attachment = {"fileName": filename, "contentType": ty, "comment": files[filename]}
        f = open(filename, "rb")
        try:
            byts = f.read()
            logging.info("calling addAttachment(%s, %s, %s, ...)", token, existing_page["id"], repr(attachment))
            server.confluence1.addAttachment(token, existing_page["id"], attachment, xmlrpclib.Binary(byts))
            logging.info("done")
        except Exception:
            logging.exception("Unable to attach %s", filename)
        finally:
            f.close()


@deprecate_xmlrpc_notification
def remove_all_attachments(server, token, space, title):
    existing_page = server.confluence1.getPage(token, space, title)

    # Get a list of attachments
    files = server.confluence1.getAttachments(token, existing_page["id"])

    # Iterate through them all, removing each
    numfiles = len(files)
    i = 0
    for f in files:
        filename = f['fileName']
        print("Removing %d of %d (%s)..." % (i, numfiles, filename))
        server.confluence1.removeAttachment(token, existing_page["id"], filename)
        i += 1


@deprecate_xmlrpc_notification
def write_page(server, token, space, title, content, parent=None):
    parent_id = None
    if parent is not None:
        try:
            # Find out the ID of the parent page
            parent_id = server.confluence1.getPage(token, space, parent)['id']
            print("parent page id is %s" % parent_id)
        except:
            print("couldn't find parent page; ignoring error...")

    try:
        existing_page = server.confluence1.getPage(token, space, title)
    except:
        # In case it doesn't exist
        existing_page = {"space": space, "title": title}

    if parent_id is not None:
        existing_page["parentId"] = parent_id

    existing_page["content"] = content
    existing_page = server.confluence1.storePage(token, existing_page)


class Confluence(object):

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
        def find_file(path):
            """
            Find the file named path in the sys.path.
            Returns the full path name if found, None if not found
            """
            paths = [os.getcwd(), '.', os.path.expanduser('~')]
            paths.extend(sys.path)
            for dir_name in paths:
                possible = os.path.abspath(os.path.join(dir_name, path))
                if os.path.isfile(possible):
                    return possible
            return None

        config = ConfigParser.ConfigParser(defaults={'user': username, 'pass': password, 'appid': appid})

        config_file = find_file('config.ini')
        if config_file:
            logging.debug("Found %s config file" % config_file)

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

        self.logging = logging

        socket.setdefaulttimeout(120)  # without this there is no timeout, and this may block the requests
        # 60 - getPages() timeout one with this !
        self._server = xmlrpclib.ServerProxy(
            options['server'] +
            '/rpc/xmlrpc', allow_none=True)  # using Server or ServerProxy ?

        # TODO: get rid of this split and just set self.server, self.token
        self._token = None
        self._token2 = None

        # Set the base URL for REST calls.
        self.base_url = url + '/rest/api/'

        # Create a request session.
        self.connection = requests.Session()
        self.connection.auth = HTTPBasicAuth(options['username'], options['password'])

        if not self.connection_valid():
            logging.critical('Connection is None.')

        logging.debug("Instantiated Confluence object.")

    def connection_valid(self):
        """Checks if a connection to the Confluence server can be established.

        :rtype: Boolean
        """
        try:
            result = self.connection.get(self.base_url + 'content')
            result.raise_for_status()

        except requests.exceptions.HTTPError as err:
            print(err)
            raise err

        except requests.exceptions.RequestException as err:
            logging.exception('Connection Error: {}').format(err)
            print(err)
            raise err

        if not result.ok:
            self.connection = None
        return self.connection is not None

    def get_spaces(self, timeout=10):
        """Returns all spaces on the server.

        :rtype: TODO @wowsuchnamaste insert rtype
        """

        request = self.base_url + 'space'
        response = self.connection.get(request, timeout=timeout)
        if not response.ok:
            response = False

        return response.json()

    @deprecate_xmlrpc_notification
    def getPage(self, page, space):
        """
        Returns a page object as a dictionary.

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :return: dictionary. result['content'] contains the body of the page.
        """
        if self._token2:
            page = self._server.confluence2.getPage(self._token2, space, page)
        else:
            page = self._server.confluence1.getPage(self._token, space, page)
        return page

    def get_page(self, space, page, timeout=10):
        request = self.base_url + 'content?&spaceKey={space}&title={page}'.format(
            space=space, page=page
        )

        response = self.connection.get(request, timeout=timeout)
        if not response.ok:
            response = False

        return response.json()

    def get_pages(self, space, timeout=10):
        request = self.base_url + 'content?type=page&spaceKey={space}'.format(
            space=space
        )
        response = self.connection.get(request, timeout=timeout)
        if not response.ok:
            response = False

        return response.json()['results']

    @deprecate_xmlrpc_notification
    def getAttachments(self, page, space):
        """
        Returns a attachments as a dictionary.

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :return: dictionary. result['content'] contains the body of the page.
        """
        if self._token2:
            server = self._server.confluence2
            token = self._token2
        else:
            server = self._server.confluence1
            token = self._token1
        existing_page = server.getPage(token, space, page)
        try:
            attachments = server.getAttachments(token, existing_page["id"])
        except xmlrpclib.Fault:
            logging.info("No existing attachment")
            attachments = None
        return attachments

    @deprecate_xmlrpc_notification
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
        if self._token2:
            server = self._server.confluence2
            token = self._token2
        else:
            server = self._server.confluence1
            token = self._token1
        existing_page = server.getPage(token, space, page)
        try:
            DATA = server.getAttachmentData(token, existing_page["id"], fileName, "0")
        except xmlrpclib.Fault:
            logging.info("No existing attachment")
            DATA = None
        return DATA

    @deprecate_xmlrpc_notification
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
        if self._token2:
            server = self._server.confluence2
            token = self._token2
        else:
            server = self._server.confluence1
            token = self._token1
        existing_page = server.getPage(token, space, page)
        for filename in files.keys():
            try:
                server.removeAttachment(token, existing_page["id"], filename)
            except xmlrpclib.Fault:
                logging.info("No existing attachment to replace")
            content_types = {
                "gif": "image/gif",
                "png": "image/png",
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "pdf": "application/pdf",
            }
            extension = os.path.splitext(filename)[1:]
            ty = content_types.get(extension, "application/binary")
            attachment = {"fileName": filename, "contentType": ty, "comment": files[filename]}
            f = open(filename, "rb")
            try:
                byts = f.read()
                logging.info("calling addAttachment(%s, %s, %s, ...)", token, existing_page["id"], repr(attachment))
                server.addAttachment(token, existing_page["id"], attachment, xmlrpclib.Binary(byts))
                logging.info("done")
            except xmlrpclib.Error:
                logging.exception("Unable to attach %s", filename)
            finally:
                f.close()

    @deprecate_xmlrpc_notification
    def getBlogEntries(self, space):
        """
        Returns a page object as a Vector.

        :param space: The space name
        :type  space: ``str``
        """
        if self._token2:
            entries = self._server.confluence2.getBlogEntries(self._token2, space)
        else:
            entries = self._server.confluence1.getBlogEntries(self._token, space)
        return entries

    @deprecate_xmlrpc_notification
    def getBlogEntry(self, pageId):
        """
        Returns a blog page as a BlogEntry object.

        :param pageId:
        """
        if self._token2:
            entry = self._server.confluence2.getBlogEntry(self._token2, pageId)
        else:
            entry = self._server.confluence1.getBlogEntries(self._token, pageId)
        return entry

    @deprecate_xmlrpc_notification
    def storeBlogEntry(self, entry):
        """
        Store or update blog content.
        (The BlogEntry given as an argument should have space, title and content fields at a minimum.)

        :param entry: Blog entry
        :type  entry: ``str``

        :rtype: ``bool``
        :return: `true` if succeeded
        """
        if self._token2:
            blogEntry = self._server.confluence2.storeBlogEntry(self._token2, entry)
        else:
            blogEntry = self._server.confluence1.storeBlogEntry(self._token2, entry)
        return blogEntry

    @deprecate_xmlrpc_notification
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
        if self._token2:
            ret = self._server.confluence2.addLabelByName(self._token2, labelName, objectId)
        else:
            ret = self._server.confluence1.addLabelByName(self._token, labelName, objectId)
        return ret

    @deprecate_xmlrpc_notification
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
        if self._token2:
            page = self._server.confluence2.getPage(self._token2, space, page)
        else:
            page = self._server.confluence1.getPage(self._token, space, page)
        return page['id']

    def get_page_id(self, space, page, timeout=10):
        """
        Returns the numeric id of a Confluence page.

        :param space: The space name.
        :type  space: ``str``

        :param page: The page name.
        :type  page: ``str``

        :param timeout: Timeout in seconds.
        :type  timeout: ``int``

        :rtype ``int``
        :return: Page numeric id.
        """
        request = self.base_url + 'content?type=page&spaceKey={space}&title={page}'.format(
            space=space, page=page
        )

        response = self.connection.get(request, timeout=timeout)
        if not response.ok:
            response = False

        return int(response.json()['results'][0]['id'])

    @deprecate_xmlrpc_notification
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

        if not targetPageId.isdigit():
            targetPageId = self.getPageId(targetPageId, space)
        for sourcePageId in sourcePageIds:
            if not sourcePageId.isdigit():
                sourcePageId = self.getPageId(sourcePageId, space)

            if self._token2:
                self._server.confluence2.movePage(self._token2,
                                                  str(sourcePageId), str(targetPageId), position)
            else:
                self._server.confluence1.movePage(self._token2,
                                                  str(sourcePageId), str(targetPageId), position)

    @deprecate_xmlrpc_notification
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

        try:
            data = self.getPage(page, space)
        except xmlrpclib.Fault:
            data = {
                "space": space,
                "title": page
            }

        data['content'] = content

        if parent_page:
            parent_id = self.getPageId(parent_page, space)
            data["parentId"] = parent_id

        if self._token2:
            if convert_wiki:
                content = self._server.confluence2.convertWikiToStorageFormat(self._token2, content)
            data['content'] = content
            return self._server.confluence2.storePage(self._token2, data)
        else:
            return self._server.confluence1.storePage(self._token, data)

    @deprecate_xmlrpc_notification
    def renderContent(self, space, page, a='', b={'style': 'clean'}):
        """
        Obtains the HTML content of a wiki page.

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :return: string: HTML content
        """

        try:
            if not page.isdigit():
                page = self.getPageId(page=page, space=space)
            if self._token2:
                return self._server.confluence2.renderContent(self._token2, space, page, a, b)
            else:
                return self._server.confluence1.renderContent(self._token, space, page, a, b)
        except ssl.SSLError as err:
            logging.error("%s while retrieving page %s", err, page)
            return None
        except xmlrpclib.Fault as err:
            logging.error("Failed call to renderContent('%s','%s') : %d : %s", space, page, err.faultCode, err.faultString)
            raise err

    @deprecate_xmlrpc_notification
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
        if self._token2:
            return self._server.confluence2.convertWikiToStorageFormat(self._token2, markup)
        else:
            return self._server.confluence.convertWikiToStorageFormat(self._token2, markup)

    @deprecate_xmlrpc_notification
    def getSpaces(self):
        # return self._server.confluence2.getSpaces(self._token2)
        return self.get_spaces()

    @deprecate_xmlrpc_notification
    def getPages(self, space):
        """
        Get pages in a space

        :param space: The space name
        :type  space: ``str``

        :rtype: ``list``
        :return: a list of pages in a space
        """
        return self._server.confluence2.getPages(self._token2, space)

    @deprecate_xmlrpc_notification
    def getPagesWithErrors(self, stdout=True, caching=True):
        """
        Get pages with formatting errors
        """
        result = []
        cnt = 0
        cnt_err = 0
        stats = {}
        data = {}
        pages = {}
        if caching:
            try:
                data = json.load(open('pages.json', 'r'))
                pages = copy.deepcopy(data)
                logging.info("%s pages loaded from cache.", len(pages.keys()))
            except IOError:
                pass
        if not data:
            spaces = self.getSpaces()
            for space in spaces:
                logging.debug("Space %s", space['key'])
                for page in self.getPages(space=space['key']):
                    pages[page['id']] = page['url']
            logging.info("%s pages loaded from confluence.", len(pages.keys()))

        for page in sorted(pages.keys()):
            cnt += 1

            renderedPage = self.renderContent(None, page, '', {'style': 'clean'})

            if not renderedPage:
                if "Render failed" in stats:
                    stats['Render failed'] += 1
                else:
                    stats['Render failed'] = 1
                if stdout:
                    print("\n%s" % page['url'])
                cnt_err += 1
                result.insert(-1, page['url'])
                data[page] = pages[page]
                continue
            if renderedPage.find('<div class="error">') > 0:
                t = re.findall('<div class="error">(.*?)</div>', renderedPage, re.IGNORECASE | re.MULTILINE)
                for x in t:
                    print("\n    %s" % t)
                    if x not in stats:
                        stats[x] = 1
                    else:
                        stats[x] += 1
                if stdout:
                    print("\n%s" % pages[page])
                cnt_err += 1
                result.insert(-1, pages[page])
                data[page] = pages[page]
            elif stdout:
                print("\r [%s/%s]" % (cnt_err, cnt), end='')

        json.dump(data, open('pages.json', 'w+'), indent=1)

        if stdout:
            print("-- stats --")
            for x in stats:
                print("'%s' : %s" % (x, stats[x]))
        return result
