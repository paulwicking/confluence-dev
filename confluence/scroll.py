from confluence import Confluence

conf = Confluence('profile')
space_key = 'space key'
page = 'title of root page'
root_page_id = conf.get_page_id(space_key, page)


def space_attributes_to_set(space_key):
    """Query whether user wants to add, remove, set or clear attributes."""
    user_choice_action = input('Do you want to [s]et or [c]lear attributes?')
    while user_choice_action != 's' or 'c':
        print(f"Your choice {user_choice_action} is not linked to an action.\n"
              f" You must choose among [s]et, [a]dd, [r]emove and [c]lear.")

    # Query available attributes and their values
    response = conf.connection.get(conf.base_url + f'/rest/scroll-versions/1.0/attribute/{space_key}')
    for item in response:
        # foreach($Attribute in $Response)
        # {
        #     foreach($Value in $Attribute.values)
        # {
            # $OutObj | Add - Member - MemberType: NoteProperty - Name:'Attributename' - Value:$Attribute.name
            # $OutObj | Add - Member - MemberType: NoteProperty - Name:'Attributeid' - Value:$Attribute.id
            # $OutObj | Add - Member - MemberType: NoteProperty - Name:'Valuename' - Value:$Value.name
            # $OutObj | Add - Member - MemberType: NoteProperty - Name:'Valueid' - Value:$Value.id
            # $AvailableAttributeList += $OutObj
            # }

        print(f"Found the following attributes for space {space_key}:")
            for num, attribute, value in AvailableAttributeList
                print(f"{i}): {attribute}: {value}")

    UserChoice = input("Please enter a comma-separated list of attributes (by index) you want to set:")
    while not UserChoice:
        print("ERROR: You must specify at least a single attribute value to set.")
    TargetAttributeList = input()

    for item in UserChoice.split(","):
        # $Index = [int]::Parse($Item.Trim())
        # if ($Index -lt 0 - or $Index -gt $AvailableAttributeList.Count)
        #     throw "ERROR: Input value '$Index' is out of range."
        #
        # $TargetAttributeList += $AvailableAttributeList[$Index]
        pass

    return UserChoiceAction, TargetAttributeList

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
