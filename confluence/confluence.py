#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from requests.auth import HTTPBasicAuth

# import copy
# import json
import logging
import os
# import re
import requests
import socket
# import ssl
import sys

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

log = logging.getLogger(__name__)


class Confluence(object):

    DEFAULT_OPTIONS = {
        "server": "http://localhost:8090",
        "verify": True
    }

    def __init__(self, profile=None, url="http://localhost:8090/", username=None, password=None, app_id=None, debug=False):
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

        config = ConfigParser.SafeConfigParser(defaults={'user': username, 'pass': password, 'app_id': app_id})

        config_file = find_file('config.ini')
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
                app_id = config.get(profile, 'app_id')
            else:
                raise EnvironmentError(
                    '%s was not able to locate the config.ini file.\n'
                    'config.ini must be in current directory, user home directory or PYTHONPATH.'
                    % __name__)

        options = Confluence.DEFAULT_OPTIONS
        options['base_url'] = url
        options['username'] = username
        options['password'] = password

        self.connection = requests.Session()
        self.connection.auth = HTTPBasicAuth(options['username'], options['password'])

        socket.setdefaulttimeout(120)  # without this there is no timeout, and this may block the requests
        # 60 - getPages() timeout one with this !
        self._server = options['base_url'] + '/rest/api/'

        if not self.connection_valid():
            log.critical('Could not establish a valid connection. Check configuration.')

        log.debug("Instantiated object.")

    def connection_valid(self):
        """Checks if a connection to the Confluence server can be established.

        :rtype: Boolean
        """
        try:
            result = self.connection.get(self._server + 'content')
        except requests.ConnectionError as err:
            log.exception('Connection Error: Check username, password and url.')
            raise err

        if not result.ok:
            self.connection = None
        return self.connection is not None

    def getPage(self, page, space):
        """
        Returns a page object as a dictionary.

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :return: dictionary. result['content'] contains the body of the page.
        """
#        if self._token2:
#            page = self._server.confluence2.getPage(self._token2, space, page)
#        else:
#            page = self._server.confluence1.getPage(self._token, space, page)
#        return page

    def get_page(self, page, space, limit=None):  # TODO: Finish method
        """Returns a page as dict.

        Returns a page object as a dictionary.

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :param limit: Specify the number of pages to return. Defaults to Confluence's API default.
        :type  limit: ``int``

        :return: dictionary. result['content'] contains the body of the page.
        """

        request = self._server + 'content?title=' + page + '&spaceKey=' + space
        # if limit:  # TODO: implement limit for this call
        #     request = request + '?limit={}'.format(limit)
        response = self.connection.get(request)
        if not response.ok:
            return None
        try:
            result = response.json()
        except ValueError:
            log.exception("Could not parse JSON data when calling method")

        return result

    def getAttachments(self, page, space):
        """
        Returns a attachments as a dictionary.

        :param page: The page name
        :type  page: ``str``

        :param space: The space name
        :type  space: ``str``

        :return: dictionary. result['content'] contains the body of the page.
        """
#        if self._token2:
#            server = self._server.confluence2
#            token = self._token2
#        else:
#            server = self._server.confluence1
#            token = self._token1
#        existing_page = server.getPage(token, space, page)
#        # try:
#        #     attachments = server.getAttachments(token, existing_page["id"])
#        # except xmlrpclib.Fault:
#        #     logging.info("No existing attachment")
#        #     attachments = None
#        return attachments
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
#        if self._token2:
#            server = self._server.confluence2
#            token = self._token2
#        else:
#            server = self._server.confluence1
#            token = self._token1
#        existing_page = server.getPage(token, space, page)
#        # try:
#        #     DATA = server.getAttachmentData(token, existing_page["id"], fileName, "0")
#        # except xmlrpclib.Fault:
#        #     logging.info("No existing attachment")
#        #     DATA = None
#        # return DATA
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
        """
        if self._token2:
            server = self._server.confluence2
            token = self._token2
        else:
            server = self._server.confluence1
            token = self._token1
        existing_page = server.getPage(token, space, page)
        for filename in files.keys():
            # try:
            #     server.removeAttachment(token, existing_page["id"], filename)
            # except xmlrpclib.Fault:
            #     logging.info("No existing attachment to replace")
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
            # f = open(filename, "rb")
            # try:
            #     byts = f.read()
            #     logging.info("calling addAttachment(%s, %s, %s, ...)", token, existing_page["id"], repr(attachment))
            #     server.addAttachment(token, existing_page["id"], attachment, xmlrpclib.Binary(byts))
            #     logging.info("done")
            # except xmlrpclib.Error:
            #     logging.exception("Unable to attach %s", filename)
            # finally:
            #     f.close()
        """
        pass

    def getBlogEntries(self, space):
        """
        Returns a page object as a Vector.

        :param space: The space name
        :type  space: ``str``
        """
#        if self._token2:
#            entries = self._server.confluence2.getBlogEntries(self._token2, space)
#        else:
#            entries = self._server.confluence1.getBlogEntries(self._token, space)
#        return entries
        pass

    def getBlogEntry(self, pageId):
        """
        Returns a blog page as a BlogEntry object.

        :param pageId:
        """
#        if self._token2:
#            entry = self._server.confluence2.getBlogEntry(self._token2, pageId)
#        else:
#            entry = self._server.confluence1.getBlogEntries(self._token, pageId)
#        return entry
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
#        if self._token2:
#            blogEntry = self._server.confluence2.storeBlogEntry(self._token2, entry)
#        else:
#            blogEntry = self._server.confluence1.storeBlogEntry(self._token2, entry)
#        return blogEntry
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
#        if self._token2:
#            ret = self._server.confluence2.addLabelByName(self._token2, labelName, objectId)
#        else:
#            ret = self._server.confluence1.addLabelByName(self._token, labelName, objectId)
#        return ret
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
#        if self._token2:
#            page = self._server.confluence2.getPage(self._token2, space, page)
#        else:
#            page = self._server.confluence1.getPage(self._token, space, page)
#        return page['id']
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

#        if not targetPageId.isdigit():
#            targetPageId = self.getPageId(targetPageId, space)
#        for sourcePageId in sourcePageIds:
#            if not sourcePageId.isdigit():
#                sourcePageId = self.getPageId(sourcePageId, space)
#
#            if self._token2:
#                self._server.confluence2.movePage(self._token2,
#                                                  str(sourcePageId), str(targetPageId), position)
#            else:
#                self._server.confluence1.movePage(self._token2,
#                                                  str(sourcePageId), str(targetPageId), position)
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
        """
        try:
            data = self.getPage(page, space)
        # except xmlrpclib.Fault:
        #     data = {
        #         "space": space,
        #         "title": page
        #     }

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

#        try:
#            if not page.isdigit():
#                page = self.getPageId(page=page, space=space)
#            if self._token2:
#                return self._server.confluence2.renderContent(self._token2, space, page, a, b)
#            else:
#                return self._server.confluence1.renderContent(self._token, space, page, a, b)
#        except ssl.SSLError as err:
#            logging.error("%s while retrieving page %s", err, page)
#            return None
        # except xmlrpclib.Fault as err:
        #     logging.error("Failed call to renderContent('%s','%s') : %d : %s", space, page, err.faultCode, err.faultString)
        #     raise err
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
        # if self._token2:
        #     return self._server.confluence2.convertWikiToStorageFormat(self._token2, markup)
        # else:
        #     return self._server.confluence.convertWikiToStorageFormat(self._token2, markup)
        pass

    #  pending deprecation: use get_spaces() in the future
    def getSpaces(self):
        function_name = str(sys._getframe().f_code.co_name) + '()'
        log.warning("Deprecated: %s. Passing to new function, using default result limit.", function_name)
        return self.get_spaces(results='clean')

    def get_spaces(self, limit=None, results=None):
        """Returns n spaces on the server as dictionary, where n is limit.

        :param limit: Specify the number of spaces to return. Defaults to Confluence's API default.
        :type  limit: ``int``

        :param results: Optional specifier for result formatting. None or clean. 'clean' mimics old behavior.
        :type  results: ``str``

        :rtype: ``dict`` or None.
        :return: List of spaces on the server up to limit, or None if the request fails.
        """
        request = self._server + 'space'
        if limit:
            request = request + '?limit={}'.format(limit)
        response = self.connection.get(request)
        if not response.ok:
            status = response.status_code
            log.debug("Response not okay: %s", status)
            return None
        try:
            result = response.json()
        except ValueError:
            log.exception("Could not parse JSON data when calling get_soaces()")
            return None
            pass

        # Clean results mimics the old behavior (response from xmlrpc connection)
        # This should probably be removed in future versions.
        if str(results).lower() == 'clean':
            clean_results = []
            base_url = result['_links']['base'] + '/display/'
            for entry in result['results']:
                clean_results.append(
                    {'key': entry['key'],
                     'name': entry['name'],
                     'type': entry['type'],
                     'url': base_url + entry['key']})
            log.debug("Spaces returned with clean results.")
            return clean_results

        return result

    def getPages(self, space):
        """
        Get pages in a space

        :param space: The space name
        :type  space: ``str``

        :rtype: ``list``
        :return: a list of pages in a space
        """
        # return self._server.confluence2.getPages(self._token2, space)
        pass

    def getPagesWithErrors(self, stdout=True, caching=True):
        """
        Get pages with formatting errors
        """
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
        """
        pass


"""
# TODO: replace all of these with object methods. Leaving for backwards compatibility for now
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
        # f = open(filename, "rb")
        # try:
        #     byts = f.read()
        #     logging.info("calling addAttachment(%s, %s, %s, ...)", token, existing_page["id"], repr(attachment))
        #     server.confluence1.addAttachment(token, existing_page["id"], attachment, xmlrpclib.Binary(byts))
        #     logging.info("done")
        # except Exception:
        #     logging.exception("Unable to attach %s", filename)
        # finally:
        #     f.close()


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


class WikiString(str):
    pass


class XMLString(str):
    pass

"""
