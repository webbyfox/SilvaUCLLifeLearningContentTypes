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
from interfaces import ICaseStudy, ICaseStudyVersion
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
                                
class CaseStudy(CatalogedVersionedContent):
    """
    Simple Course type object for Course object
    """
    implements(ICaseStudy)
    security = ClassSecurityInfo()
    meta_type = "Case Study"
    __doc__ = "Case Study object "

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
        if ICaseStudyVersion.providedBy(version):
            version.set_subjects(handler.metadata['subjects'])
            version.set_category(handler.metadata['category'])
            version.set_format(handler.metadata['format'])
            version.set_shortdescription(handler.metadata['shortdescription'][0])
    
            version.set_image(handler.metadata['image'][0])
            version.set_document(handler.metadata['document'][0]) 
         

        version.set_title(handler.title)

class CaseStudyVersion(CatalogedVersion):           
    """Base class for course object versions
    """        
    implements(ICaseStudyVersion)
    security = ClassSecurityInfo()
    meta_type = "Case Study Version"

    def __init__(self,id):
        super(CaseStudyVersion, self).__init__(id)
       
        self._shortdescription = ""
        self._subjects = ""
        self._category = ""
        self._format = ""
        self._image = ""
        self._document = ""
        self.content = SilvaXMLAttribute('content') 
        

    
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
    def set_subjects(self, subjects):
        self._subjects  = subjects 

    # Accessor
    def get_subjects(self):
        if not hasattr(self, '_subjects'):
            self._subjects  = ""
        else:
            return self._subjects

    # Mutator
    def set_category(self,category):
        self._category = category

    # Accessor
    def get_category(self):
        if not hasattr(self, '_category'):
            self._category = ""
        else:
            return self._category

    # Mutator
    def set_format(self,format):
        self._format = format

    # Accessor
    def get_format(self):
        if not hasattr(self, '_format'):
            self._format = ""
        else:
            return self._format

  
    # Mutator
    def set_image(self,image):
        self._image = image

    # Accessor
    def get_image(self):
        if not hasattr(self, '_image'):
            self._image = ""
        else:
            return self._image
     

    # Mutator
    def set_document(self,document):
        self._document = document

    # Accessor
    def get_document(self):
        if not hasattr(self, '_document'):
            self._document = ""
        else:
            return self._document

   
     
                
InitializeClass(CaseStudy)
InitializeClass(CaseStudyVersion)
