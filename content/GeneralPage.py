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
from interfaces import IGeneralPage, IGeneralPageVersion
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
                                
class GeneralPage(CatalogedVersionedContent):
    """
    Simple Course type object for Course object
    """
    implements(IGeneralPage)
    security = ClassSecurityInfo()
    meta_type = "General Page"
    __doc__ = "General Page object"

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
        if IGeneralPageVersion.providedBy(version):
            version.set_shortdescription(handler.metadata['shortdescription'][0])
            version.set_url(handler.metadata['url'][0])
            version.set_image(handler.metadata['image'][0])
            version.set_document(handler.metadata['document'][0]) 

        version.set_title(handler.title)

class GeneralPageVersion(CatalogedVersion):           
    """Base class for course object versions
    """        
    implements(IGeneralPageVersion)
    security = ClassSecurityInfo()
    meta_type = "General Page Version"

    def __init__(self,id):
        super(GeneralPageVersion, self).__init__(id)
       
        self._shortdescription = ""
        self._url = ""
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
    def set_url(self, url):
        self._url = url

    # Accessor
    def get_url(self):
        if not hasattr(self, '_url'):
            self._url = ""
        else:
            return self._url

    
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

   
     
                
InitializeClass(GeneralPage)
InitializeClass(GeneralPageVersion)
