# Copyright (c) 2013 University College London. All rights reserved.
# Author: Rizwan Mansuri (WAMS - UCL) 


# Zope
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from zope.interface import implements


# Silva
from Products.Silva import SilvaPermissions
from Products.Silva.Content import Content
from Products.Silva import mangle

# Others
from interfaces import ITags


def manage_addTags(self, id, title, result, REQUEST=None):
    """Add course tean"""
    if not mangle.Id(self,id).isValid():
        return
    object = Tags(id)
    self._setObject(id, object)
    object = getattr(self, id)
    object.set_title(title)
    add_and_edit(self, id, REQUEST)
    return object

class Tags(Content, SimpleItem):
    """
    Simple Course tags type object for Course object
    """
    implements(ITags)
    security = ClassSecurityInfo()
    meta_type = 'Course Tags'

    def __init__(self,id):
        Tags.inheritedAttribute('__init__')(self,id)
        self._subject = ""
        self._category = ""
        self._format = ""
       

    security.declareProtected(SilvaPermissions.AccessContentsInformation,'can_set_title')
    def can_set_title(self):
        return True

    security.declareProtected(SilvaPermissions.AccessContentsInformation,'is_deletable')
    def is_deletable(self):
        return True

    # Mutator 
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'set_subject')
    def set_subject(self, subject):
        self._subject = subject
    
    # Accessor 
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'get_subject')
    def get_subject(self):
        return self._subject

    # Mutator 
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'set_category')
    def set_category(self, category):
        self._category = category

    # Accessor 
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'get_category')
    def get_category(self):
        return self._category
    
    # Mutator
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'set_format')
    def set_format(self, format):
        self._format = format

    # Accessor 
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'get_format')
    def get_format(self):
        return self._format
    
 
InitializeClass(Tags)
