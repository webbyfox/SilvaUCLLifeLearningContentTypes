# Copyright (c) 2013 University College London. All rights reserved.

from zope.interface import implements
import re

# Python
from StringIO import StringIO
from xml.sax import parseString
from xml.sax.handler import ContentHandler

# Zope
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem


# Silva
from Products.Silva import SilvaPermissions
from Products.Silva.VersionedContent import CatalogedVersionedContent
from Products.Silva.Version import CatalogedVersion
from Products.Silva.interfaces import IVersionedContent
from Products.Silva.helpers import add_and_edit
from Products.Silva.Metadata import export_metadata
from Products.Silva.Content import Content
from Products.Silva import mangle

from interfaces import ICourseDate
from Products.SilvaUCLLifeLearningContentTypes.silvaxmlattribute import SilvaXMLAttribute
from Products.SilvaDocument.transform.Transformer import EditorTransformer
from Products.SilvaDocument.transform.base import Context
from Products.Silva.Image import havePIL
from DateTime import DateTime


def manage_addCourseDate(self, id, title, result, REQUEST=None):
    """Add course date"""
    if not mangle.Id(self,id).isValid():
        return
    object = CourseDate(id)
    self._setObject(id, object)
    object = getattr(self, id)
    object.set_title(title)
    add_and_edit(self, id, REQUEST)
    return object

class CourseDate(Content, SimpleItem):
    """
    Simple Course date type object for Course object
    """
    implements(ICourseDate)
    security = ClassSecurityInfo()
    meta_type = 'Course Date'

    def __init__(self,id):
        CourseDate.inheritedAttribute('__init__')(self,id)
        self._applylink = ""
        self._coursedate = DateTime()
        self._online = True
        self._status = ""
    security.declareProtected(SilvaPermissions.AccessContentsInformation,'can_set_title')
    def can_set_title(self):
        return True

    security.declareProtected(SilvaPermissions.AccessContentsInformation,'is_deletable')
    def is_deletable(self):
        return True

    # Mutator of ApplyLink field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'set_applylink')
    def set_applylink(self, ApplyLink):
        self._applylink = ApplyLink

    # Accessor of ApplyLink field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'get_applylink')
    def get_applylink(self):
        return self._applylink

    # Mutator of CourseDate field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'set_coursedate')
    def set_coursedate(self, CourseDate):
        self._coursedate = CourseDate

    # Accessor of CourseDate field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'get_coursedate')
    def get_coursedate(self):
        return self._coursedate 
    
    # Mutator of Online field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'set_online')
    def set_online(self, Online):
        self._online = Online

    # Accessor of Online field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'get_online')
    def get_online(self):
        return self._online 
  
    # Mutator of Status field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'set_status')
    def set_status(self, Status):
        self._status = Status

    # Accessor of Status field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'get_status')
    def get_status(self):
        return self._status

   
    
InitializeClass(CourseDate)
