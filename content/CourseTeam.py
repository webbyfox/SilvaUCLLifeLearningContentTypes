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
from interfaces import ICourseTeam


def manage_addCourseTeam(self, id, title, result, REQUEST=None):
    """Add course tean"""
    if not mangle.Id(self,id).isValid():
        return
    object = CourseTeam(id)
    self._setObject(id, object)
    object = getattr(self, id)
    object.set_title(title)
    add_and_edit(self, id, REQUEST)
    return object

class CourseTeam(Content, SimpleItem):
    """
    Simple Course team type object for Course object
    """
    implements(ICourseTeam)
    security = ClassSecurityInfo()
    meta_type = 'Course Team'

    def __init__(self,id):
        CourseTeam.inheritedAttribute('__init__')(self,id)
        self._fullname = ""
        self._description = ""
        self._image = ""
        self.iris_link = ""


    security.declareProtected(SilvaPermissions.AccessContentsInformation,'can_set_title')
    def can_set_title(self):
        return True

    security.declareProtected(SilvaPermissions.AccessContentsInformation,'is_deletable')
    def is_deletable(self):
        return True

    # Mutator 
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'set_fullname')
    def set_fullname(self, fullname):
        self._fullname = fullname
    
    # Accessor 
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'get_fullname')
    def get_fullname(self):
        return self._fullname

    # Mutator 
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'set_description')
    def set_description(self, description):
        self._description = description

    # Accessor 
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'get_description')
    def get_description(self):
        return self._description
    
    # Mutator
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'set_image')
    def set_image(self, image):
        self._image = image

    # Accessor 
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'get_image')
    def get_image(self):
        return self._image 
  
    # Mutator 
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'set_iris_link')
    def set_iris_link(self, iris_link):
        self._iris_link = iris_link

    # Accessor of Status field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'get_iris_link')
    def get_iris_link(self):
        return self._iris_link
    
 
InitializeClass(CourseTeam)
