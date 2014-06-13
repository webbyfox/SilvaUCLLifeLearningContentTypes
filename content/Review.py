# Copyright (c) 2014 University College London. All rights reserved
# Author: Rizwan Mansuri (WAMS - UCL)

#Zope import
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo
from zope.interface import implements

# Silva import
from Products.Silva import mangle
from Products.Silva.Content import Content
from Products.Silva import SilvaPermissions

# Others
from interfaces import IReview

def manage_addReview(self, id, title, result, REQUEST=None):
    """Add review"""
    if not mangle.Id(self,id).isValid():
        return
    object = Review(id)
    self._setObject(id, object)
    object = getattr(self, id)
    object.set_title(title)
    add_and_edit(self, id, REQUEST)
    return object

class Review(Content, SimpleItem):
    """
    Reviews for Course Object
    """
    implements(IReview)
    security = ClassSecurityInfo()
    meta_type = "Review"

    def __init__(self, id):
        Review.inheritedAttribute('__init__')(self,id)
        self._reviewmembername = ""
        self._reviewmembertitle = ""
        self._reviewmemberdescription = ""
        self._reviewmemberimagepath = ""

    security.declareProtected(SilvaPermissions.AccessContentsInformation, 'can_set_title')
    def can_set_title(self):
        return True

    security.declareProtected(SilvaPermissions.AccessContentsInformation, 'is_deletable')
    def is_deletable(self):
        return True

    # Mutator for ReviewMemberName field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent, 'set_reviewmembername')
    def set_reviewmembername(self, ReviewMemberName):
        self._reviewmembername = ReviewMemberName

    # Accessor for ReviewMemberName field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent, 'get_reviewmembername')
    def get_reviewmembername(self):
        return self._reviewmembername
    
    
    # Mutator for ReviewMemberTitle field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent, 'set_reviewmembertitle')
    def set_reviewmembertitle(self, ReviewMemberTitle):
        self._reviewmembertitle = ReviewMemberTitle

    # Accessor for ReviewMemberTitle field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent, 'get_reviewmembertitle')
    def get_reviewmembertitle(self):
        return self._reviewmembertitle

    
    # Mutator for ReviewMemberDescription field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent, 'set_reviewmemberdescription')
    def set_reviewmemberdescription(self, ReviewMemberDescription):
        self._reviewmemberdescription = ReviewMemberDescription

    # Accessor for ReviewMemberDescription field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent, 'get_reviewmemberdescription')
    def get_reviewmemberdescription(self):
        return self._reviewmemberdescription

    
    # Mutator for ReviewMemberImagePath field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent, 'set_reviewmemberimagepath')
    def set_reviewmemberimagepath(self, ReviewMemberImagePath):
        self._reviewmemberimagepath = ReviewMemberImagePath

    # Accessor for ReviewMemberImagePath field
    security.declareProtected(SilvaPermissions.ChangeSilvaContent, 'get_reviewmemberimagepath')
    def get_reviewmemberimagepath(self):
        return self._reviewmemberimagepath


