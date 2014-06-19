# Copyright (c) 2014 University College London. All rights reserved.


# Python
from StringIO import StringIO
from xml.sax import parseString
from xml.sax.handler import ContentHandler 

# Zope
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from zope.interface import implements


# Silva
from Products.Silva import SilvaPermissions
from Products.Silva.Folder import Folder
from Products.Silva import mangle
from Products.Silva.VersionedContent import CatalogedVersionedContent
from Products.Silva.Version import CatalogedVersion

# not sure next three lines uses in code or not...removed it if not
from Products.Silva.interfaces import IVersionedContent
from Products.Silva.helpers import add_and_edit
from Products.Silva.Metadata import export_metadata



# Others
from interfaces import ICoursePage, ICoursePageVersion
from Products.SilvaUCLLifeLearningContentTypes.silvaxmlattribute import SilvaXMLAttribute


class MetaDataSaveHandler(ContentHandler):
    
    def startDocument(self):
        self.title = "" 
        self.inside_title = False
        self.metadata = {}
    
    def startElement(self, name, attributes):
        if name == 'h2' and not self.title:
            self.inside_title = True
        elif name == 'meta':
             if (attributes.get('scheme') ==
                    'http://infrae.com/namespaces/metadata/silva-news'):
                name = attributes.get("name","")
                content = attributes.get("content", "")
                self.metadata[name] = self.parse_content(content)

    def endElement(self, name):
        if name == 'h2':
            self.inside_title = False

    def characters(self, data):
        if self.inside_title:
            self.title += data
            
    def parse_content(self, content):
        return [self.deentitize_and_deescape_pipes(x) for x in content.split('|')]                                    

    def deentitize_and_deescape_pipes(self, data):
        data = data.replace('&pipe;','|')
        data = data.replace('&lt;','<')
        data = data.replace('&gt;','>')
        data = data.replace('&quot;','"')
        data = data.replace('&amp;','&')
        return data
                                
class CoursePage(CatalogedVersionedContent):
    """
    Simple Course type object for Course object
    """
    implements(ICoursePage)
    security = ClassSecurityInfo()
    meta_type = 'Course Page'
    __doc__ = "Course Page object for Course Container"

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,'PUT')
    def PUT(self, REQUEST=None, RESPONSE=None):
        """PUT support
        """
        
        if REQUEST is None:
            REQUEST = self.REQUEST
        if RESPONSE is None:
            RESPONSE = self.RESPONSE
        
        content = REQUEST['BODYFILE'].read()
        self.save_title_and_metadata(content)
        self.get_editable().content.saveEditorHTML(content)

    def save_title_and_metadata(self, html):
        handler = MetaDataSaveHandler()
        parseString(html, handler)
        version = self.get_editable()
        if ICoursePageVersion.providedBy(version):
            version.set_pagetitle(handler.metadata['pagetitle'][0])
            version.set_shortdescription(handler.metadata['shortdescription'][0])
            version.set_adminname(handler.metadata['adminname'][0])
            version.set_adminemail(handler.metadata['adminemail'][0])
            version.set_admintelephone(handler.metadata['admintelephone'][0])
            version.set_timingaccess(handler.metadata['timingaccess'][0])
            version.set_location(handler.metadata['location'][0])
            version.set_locationurl(handler.metadata['locationurl'][0])
            version.set_cost(handler.metadata['cost'][0])
            version.set_learninghours(handler.metadata['learninghours'][0])
            version.set_courseduration(handler.metadata['courseduration'][0])

        version.set_title(handler.title)

class CoursePageVersion(CatalogedVersion):           
    """Base class for course object versions
    """        
    implements(ICoursePageVersion)
    security = ClassSecurityInfo()
    meta_type = "Course Page Version"

    def __init__(self,id):
        super(CoursePageVersion, self).__init__(id)
        self._pagetitle = ""
        self._shortdescription = ""
        self._adminname = ""
        self._adminemail = ""
        self._admintelephone = ""
        self._timingaccess = ""
        self._location = ""
        self._locationurl = ""
        self._cost = ""
        self._learninghours = ""
        self._courseduration = ""
        self.content = SilvaXMLAttribute('content') 
        

    # Mutator
    def set_pagetitle(self,pagetitle):
        self._pagetitle = pagetitle

    # Accessor
    def get_pagetitle(self):
        if not hasattr(self, '_pagetitle'):
            self._pagetitle = ""
        else:
            return self._pagetitle

    # Mutator
    def set_shortdescription(self, shortdescription):
        self._shortdescription = shortdescription

    # Accessor
    def get_shortdescription(self):
        if not hasattr(self, '_shortdescription'):
            self._shortdescription = ""
        else:
            return self._shortdescription

    # Mutator
    def set_adminname(self,adminname):
        self._adminname = adminname

    # Accessor
    def get_adminname(self):
        if not hasattr(self, '_adminname'):
            self._adminname = ""
        else:
            return self._adminname


    # Mutator
    def set_adminemail(self,adminemail):
        self._adminemail = adminemail

    # Accessor
    def get_adminemail(self):
        if not hasattr(self, '_adminemail'):
            self._adminemail = ""
        else:
            return self._adminemail
    

    # Mutator
    def set_admintelephone(self,admintelephone):
        self._admintelephone = admintelephone

    # Accessor
    def get_admintelephone(self):
        if not hasattr(self, '_admintelephone'):
            self._admintelephone = ""
        else:
            return self._admintelephone
    

    # Mutator
    def set_timingaccess(self,timingaccess):
        self._timingaccess = timingaccess

    # Accessor
    def get_timingaccess(self):
        if not hasattr(self, '_timingaccess'):
            self._timingaccess = ""
        else:
            return self._timingaccess
            

    # Mutator
    def set_location(self,location):
        self._location = location

    # Accessor
    def get_location(self):
        if not hasattr(self, '_location'):
            self._location = ""
        else:
            return self._location
     
    # Mutator
    def set_locationurl(self,locationurl):
        self._locationurl = locationurl

    # Accessor
    def get_locationurl(self):
        if not hasattr(self, '_locationurl'):
            self._locationurl = ""
        else:
            return self._locationurl
     
    # Mutator
    def set_cost(self,cost):
        self._cost = cost

    # Accessor
    def get_cost(self):
        if not hasattr(self, '_cost'):
            self._cost = ""
        else:
            return self._cost
     
    # Mutator
    def set_learninghours(self,learninghours):
        self._learninghours = learninghours

    # Accessor
    def get_learninghours(self):
        if not hasattr(self, '_learninghours'):
            self._learninghours = ""
        else:
            return self._learninghours
     
    # Mutator
    def set_courseduration(self,courseduration):
        self._courseduration = courseduration

    # Accessor
    def get_courseduration(self):
        if not hasattr(self, '_courseduration'):
            self._courseduration = ""
        else:
            return self._courseduration
     
                
InitializeClass(CoursePage)
InitializeClass(CoursePageVersion)
