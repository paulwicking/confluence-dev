from confluence import Confluence

# conf = Confluence('profile')
# space_key = 'space key'
# page = 'title of root page'
# root_page_id = conf.get_page_id(space_key, page)


class ScrollVersions(object):

    def __init__(self, confluence_instance):
        self.conf = confluence_instance
        self.scroll_base_url = self.conf.base_url

    def get_response(self):
        """Get a yes or no response from the user.

        :rtype: Boolean
        """
        positive = {'yes', 'y', 'ye', 'yeah', ''}
        negative = {'n', 'no'}

        response = input("[Y/n]: ").lower()
        if response in positive:
            return True
        elif response in negative:
            return False
        return self.get_response()

    def get_action_from_user(self):
        """Query whether user wants to add, remove, set or clear attributes."""
        available_actions = {
            'a': 'add',
            's': 'set',
            'r': 'remove',
            'c': 'clear',
        }

        response = input('Do you want to [s]et or [c]lear attributes? ').lower()

        if response not in available_actions:
            print(f'Your choice, {response}, is not linked to an action. '
                  f'You must choose among [s]et, [a]dd, [r]emove and [c]lear: ')
            return self.get_action_from_user()
        return response

    def change_attributes(self, root_page_id, attribute, action=None):
        if action is None:
            return

        pages = self.get_child_page_list(root_page_id)

        for page in pages:
            print(f'Setting attributes for page {page.title} - {page.id})')
            request = self.conf.base_url + "/rest/scroll-versions/1.0/metadata/page/{page.id})"
            response = self.conf.connection.get(request)

        return response

    def add_attributes(self, root_page_id, attribute):
        pass

    def set_attributes(self, root_page_id, attribute):
        pages = self.get_child_page_list(root_page_id)

        for page in pages:
            print(f'Setting {attribute} for page {page.title} - {page.id})')
            # request = f"{confluence_server}/rest/scroll-versions/1.0/metadata/page/{page.id})"
            # response = self.connection.get(request)

        child_pages = []

        print(f'Ready to SET the following attribute values to {len(child_pages)} child pages of page {root_page_id}.\n'
              f'Proceed?')

        user_wants_to_proceed = self.get_response()
        if user_wants_to_proceed:
            # TODO: commit changes
            pass

        # return False so we know nothing was set
        return False

    def remove_attributes(self, root_page_id, attribute):
        pass

    def clear_attributes(self, root_page_id):
        pass

    def get_credentials_from_user(self):
        username = input('Enter your Vizrt user-id: ')
        password = input('Enter your password: ')

        return username, password

    def get_space_key_from_user(self):
        space_key = input('Enter space key: ')
        return str(space_key)

    def get_root_page_id_from_user(self):
        root_page_id = input('Enter root page id: ')

        return int(root_page_id)

    def get_child_page_list(self, root_page_id):
        """Fetch all child pages of `root_page_id` on self.confluence_server"""
        child_page_list = []
        start = 0
        limit = 25
        request = self.conf.base_url + '/rest/api/content/{}/child/page?start={}&limit={}'.format(
            root_page_id, start, limit)
        response = self.conf.connection.get(request)
        for entry in response:
            child_page_list.append(entry)
        number_of_children = len(child_page_list)

        print('Found {} children:').format(number_of_children)
        for entry in child_page_list:
            print(entry)

        return child_page_list

    def get_all_available_attributes_and_values(self, space_key):
        request = '{}/rest/scroll-versions/1.0/attribute/{}'.format(self.conf.base_url, space_key)
        response = self.conf.connection.get(request).json()

        return response

    def print_available_attributes(self, available_attributes):
        print('Found the following attributes:')
        for entry in available_attributes:
            print('Attribute: ' + entry['name'])
            print('ID: ' + entry['id'])
            print('Values:')
            for value in entry['values']:
                print('        ' + value['name'])
            print(' --- --- --- --- --- --- --- --- ---')


    """
    # Query user for which attributes to set, add or remove (example: 0,2,4)
    user_choice = input("Please enter a comma-separated list of attributes (by index) you want to set")
    if user_choice is None:
        print("ERROR: You must specify at least a single attribute value to set.")
    target_attribute_list = []
    # TODO: clean up the comma-separated input, and check for legal values.
    """

#
# def space_attributes_to_set(space_key):
#     user_choice_action = input('Do you want to [s]et or [c]lear attributes?')
#     while user_choice_action != 's' or 'c':
#         print(f"Your choice {user_choice_action} is not linked to an action.\n"
#               f" You must choose among [s]et, [a]dd, [r]emove and [c]lear.")
#
#     # Query available attributes and their values
#     AvailableAttributeList = conf.connection.get(conf.base_url + f'/rest/scroll-versions/1.0/attribute/{space_key}')
#
#     for item in AvailableAttributeList:
#         # foreach($Attribute in $Response)
#         # {
#         #     foreach($Value in $Attribute.values)
#         # {
#             # $OutObj | Add - Member - MemberType: NoteProperty - Name:'Attributename' - Value:$Attribute.name
#             # $OutObj | Add - Member - MemberType: NoteProperty - Name:'Attributeid' - Value:$Attribute.id
#             # $OutObj | Add - Member - MemberType: NoteProperty - Name:'Valuename' - Value:$Value.name
#             # $OutObj | Add - Member - MemberType: NoteProperty - Name:'Valueid' - Value:$Value.id
#             # $AvailableAttributeList += $OutObj
#             # }
#         pass
#
#         print(f"Found the following attributes for space {space_key}:")
#         for num, attribute, value in AvailableAttributeList:
#             print(f"{num}: {attribute}: {value}")
#
#     UserChoice = input("Please enter a comma-separated list of attributes (by index) you want to set:")
#     while not UserChoice:
#         print("ERROR: You must specify at least a single attribute value to set.")
#     TargetAttributeList = input()
#
#     for item in UserChoice.split(","):
#         # $Index = [int]::Parse($Item.Trim())
#         # if ($Index -lt 0 - or $Index -gt $AvailableAttributeList.Count)
#         #     throw "ERROR: Input value '$Index' is out of range."
#         #
#         # $TargetAttributeList += $AvailableAttributeList[$Index]
#         pass
#
#     return UserChoice, TargetAttributeList
#
# 'c'
#
# $TargetAttributeList = $AvailableAttributeList
# Write - Host
# "All of above listed attributes will be removed. You'll have to acknowledge in a next step."
# return $UserChoiceAction, $TargetAttributeList
#
#
# def set_attributes(attribute_list):
#
#     validate_not_null_or_empty(ChildPages)
#     print(f"Ready to SET the following attribute values to {len(ChildPages)} child pages of page {root_page_id}.")
#     action = input("Do you want to continue? (y/n)")
#     if not action.lower().startswith('y'):
#         raise Exception("Aborted")
#
#     for attribute in attribute_list:
#         # $ConversionDict[$Attribute.Attributeid] += @
#         # $Attribute.Valueid =$true}
#
#         for item in ChildPages:
#             print(f"Setting attributes for page {PageItem.title} {PageItem.id}")
#
#     url = f'{ConfluenceServer}/rest/scroll-versions/1.0/metadata/page/{PageItem.id})'
#     conf.connection.post(url)
#
# def clear_attributes(attribute_list):
#     validate_not_null_or_empty(attribute_list)
#     validate_not_null_or_empty(ChildPages)
#
#     print(f"Ready to CLEAR the following attribute values from {len(ChildPages.Count)} child pages of page {root_page_id}.")
#     action = input("Do you want to continue? (y/n)")
#     if not action.lower().startswith('y'):
#         raise Exception("Aborted")
#
#     # Prepare body for request
#     ConversionDict = {}
#     for attribute in attribute_list:
#         ConversionDict[attribute.Attributeid] = attribute['id': 'false']
#
#     for PageItem in ChildPages:
#         print("Clearing attributes for page $($PageItem.title) ($($PageItem.id))")
#         url = "$ConfluenceServer/rest/scroll-versions/1.0/metadata/page/$($PageItem.id)"
#
#         conf.connection.post(url) # UserChoiceAction, $TargetAttributeList = Query - SpaceAttributesToSet - SpaceKey:$SpaceKey
#
#
# "Fetching all childpages of $RootPageId on $ConfluenceServer"
# # Get - ChildPages - RootPageId:$RootPageId
#
# "Found $($Script:ChildPageList.Count) children:"
# # Write - Host($Script: ChildPageList | Format - Table | Out - String)
#
# switch(UserChoiceAction)
#         's' # Set - Attributes - AttributeList:$TargetAttributeList - ChildPages:$ChildPageList
#         'c' # Clear - Attributes - AttributeList:$TargetAttributeList - ChildPages:$ChildPageList
# raise Exception(f"Your choice {UserChoiceAction} is not linked to an action. You must choose among [s]et or [c]lear.")
