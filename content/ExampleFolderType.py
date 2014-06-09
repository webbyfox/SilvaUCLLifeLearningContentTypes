# Copyright (c) 2013 University College London. All rights reserved.

from zope.interface import implements
from zope.component import getMultiAdapter

from interfaces import IExampleFolderType

from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.Silva.Folder import Folder
from Products.Silva.Publication import Publication
from Products.Silva import SilvaPermissions


class ExampleFolderType(Folder, Publication):
    """Example folder"""

    __doc__ = """An example folder type. Replace this or supplement to meet you needs."""

    security = ClassSecurityInfo()
    meta_type = 'Example Folder'
    implements((IExampleFolderType))
    _addables_allowed_in_publication = ['Silva Image', 'Silva Folder', 'Example Folder', 'Example Document']

    def __init__(self, id):
        ExampleFolderType.inheritedAttribute('__init__')(self, id)


    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                                   'get_components')


    def get_components(self):
        filtered_items = list(self.filter_entries(self.get_ordered_publishables()))
        return filtered_items

InitializeClass(ExampleFolderType)

