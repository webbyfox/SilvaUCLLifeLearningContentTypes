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


from interfaces import ICourseDate
from Products.SilvaUCLLifeLearningContentTypes.silvaxmlattribute import SilvaXMLAttribute
from Products.SilvaDocument.transform.Transformer import EditorTransformer
from Products.SilvaDocument.transform.base import Context
from Products.Silva.Image import havePIL
from DateTime import DateTime


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
        self._date = DateTime()

    security.declareProtected(SilvaPermissions.AccessContentsInformation,'can_set_title')
    def can_set_title(self):
        return True

    security.declareProtected(SilvaPermissions.AccessContentsInformation,'is_deletable')
    def is_deletable(self):
        return True

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'set_applylink')
    def set_applylink(self, ApplyLink):
        self._applylink = ApplyLink

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'get_applylink')
    def get_applylink(self):
        return self._applylink

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'set_date')
    def set_date(self, Date):
        self._date = Date

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'get_date')
    def get_date(self):
        return self._date

InitializeClass(CourseDate)
