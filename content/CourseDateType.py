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

# Silva
from Products.Silva import SilvaPermissions
from Products.Silva.VersionedContent import CatalogedVersionedContent
from Products.Silva.Version import CatalogedVersion
from Products.Silva.interfaces import IVersionedContent
from Products.Silva.helpers import add_and_edit
from Products.Silva.Metadata import export_metadata

from interfaces import ICourseDateType
from Products.SilvaUCLLifeLearningContentTypes.silvaxmlattribute import SilvaXMLAttribute
from Products.SilvaDocument.transform.Transformer import EditorTransformer
from Products.SilvaDocument.transform.base import Context
from Products.Silva.Image import havePIL



class MetaDataSaveHandler(ContentHandler):
    def startDocument(self):
        self.title = ''
        self.inside_title = False
        self.metadata = {}

    def startElement(self, name, attributes):
        if name == 'h2' and not self.title:
            self.inside_title = True
        elif name == 'meta':
            if (attributes.get('scheme') == 
                    'http://infrae.com/namespaces/metadata/silva-news'
                    ):
                name = attributes.get('name', '')
                content = attributes.get('content', '')
                self.metadata[name] = self.parse_content(content)
                
    def endElement(self, name):
        if name == 'h2':
            self.inside_title = False

    def characters(self, data):
        if self.inside_title:
            self.title += data

    def parse_content(self, content):
        return [self.deentitize_and_deescape_pipes(x) for 
                    x in content.split('|')]

    def deentitize_and_deescape_pipes(self, data):
        data = data.replace('&pipe;', '|')
        data = data.replace('&lt;', '<')
        data = data.replace('&gt;', '>')
        data = data.replace('&quot;', '"')
        data = data.replace('&amp;', '&')
        return data

class CourseDateType(CatalogedVersionedContent):
    """Base class for the ExampleDocumentType type.
    """
    security = ClassSecurityInfo()

    implements(ICourseDateType)
    meta_type = 'Course date object'
    __doc__ = """A Couse date object for Course container"""

    # MANIPULATORS


    # ACCESSORS
    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'to_xml')
    def to_xml(self, context):
        """Maps to the most useful(?) version
        (public, else unapproved or approved)
        """
        if context.last_version == 1:
            version_id = self.get_next_version()
            if version_id is None:
                version_id = self.get_public_version()
        else:
            version_id = self.get_public_version()

        if version_id is None:
            return

        version = getattr(self, version_id)

        context.f.write('<silva_example_document id="%s">' % self.id)
        version.to_xml(context)
        context.f.write('</silva_example_document>')

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
                                'editor_xml')
    def editor_xml(self):
        browser = 'Mozilla'
        if self.REQUEST['HTTP_USER_AGENT'].find('MSIE') > -1:
            browser = 'IE'

        context = Context(f=StringIO(),
                            last_version=1,
                            url=self.absolute_url(),
                            browser=browser,
                            model=self)
        self.to_xml(context)
        xml = context.f.getvalue()
        return xml


    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
                                'PUT')
    def PUT(self, REQUEST=None, RESPONSE=None):
        """PUT support"""
        # XXX we may want to make this more modular/pluggable at some point
        # to allow more content-types (+ transformations)
        if REQUEST is None:
            REQUEST = self.REQUEST
        if RESPONSE is None:
            RESPONSE = REQUEST.RESPONSE
        content = REQUEST['BODYFILE'].read()
        self.save_title_and_metadata(content)
        self.get_editable().content.saveEditorHTML(content)

    def save_title_and_metadata(self, html):
        handler = MetaDataSaveHandler()
        parseString(html, handler)

        version = self.get_editable()
        version.set_catalogue_number(handler.metadata['catalogue_number'][0])
        version.set_catalogue_url(handler.metadata['catalogue_url'][0])
        version.set_image_path(handler.metadata['image_path'][0])
        version.set_title(handler.title)
                 
InitializeClass(ExampleDocumentType)

class ExampleDocumentTypeVersion(CatalogedVersion):
    """Base class for ExampleDocumentTypeVersion versions.
    """
    implements(IExampleDocumentTypeVersion)
    meta_type = 'Example Document Version'
    security = ClassSecurityInfo()

    def __init__(self, id):
        # XXX dummy title?
        ExampleDocumentTypeVersion.inheritedAttribute('__init__')(self, id)
        self.content = SilvaXMLAttribute('content')
        self._catalogue_number = ''
        self._catalogue_url = ''
        self._image_path = ''


    # SETTERS
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
                              'set_catalogue_number')

    def set_catalogue_number(self, catalogue_number):
        self._catalogue_number = catalogue_number
#        self.reindex_object()

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
                              'set_catalogue_url')
    def set_catalogue_url(self, catalogue_url):
        self._catalogue_url = catalogue_url
#        self.reindex_object()

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
                                    'set_image_path')
    def set_image_path(self, image_path):
        """Sets the image_path of the component."""
        self._image_path = image_path


    # GETTERS
    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'get_catalogue_number')
    def get_catalogue_number(self):
       """Get the catalogue number of the object."""
       if not hasattr(self, '_catalogue_number'):
            self._catalogue_number = ''
       else:
            return self._catalogue_number

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                                   'get_catalogue_url')
    def get_catalogue_url(self):
       """Get the catalogue_url of the object."""
       if not hasattr(self, '_catalogue_url'):
            self._catalogue_url = ''
       else:
            return self._catalogue_url

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                                   'get_image_path')
    def get_image_path(self):
       """Get the image_path of the component."""
       if not hasattr(self, '_image_path'):
            self._image_path = ''
       else:
            return self._image_path



    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'fulltext')
    def fulltext(self):
        """Returns all data as a flat string for full text-search
        """
        s = StringIO()
        self.content.toXML(s)
        content = self._flattenxml(s.getvalue())
        return "%s %s" % (self.get_title(),
                                   content)
 
    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'to_xml')
    def to_xml(self, context):
        """Returns the content as a partial XML-document
        """
        export_metadata(self, context)

        f = context.f
        f.write(u'<title>%s</title>' % self.get_title())
        f.write(u'<meta_type>%s</meta_type>' % self.meta_type)
        # XXX really don't know how to deal with this...
        f.write(u'<sta>')
        self.content_xml(context)
        f.write(u'</sta>')
        self.content.toXML(f)

    def content_xml(self, context):
        """Writes all content elements to the XML stream"""
        f = context.f
    
    def _prepare_xml(self, inputstring):
        inputstring = inputstring.replace(u'&', u'&amp;')
        inputstring = inputstring.replace(u'<', u'&lt;')
        inputstring = inputstring.replace(u'>', u'&gt;')

        return inputstring

    # XXX had to copy this from SilvaDocument.Document...
    def _flattenxml(self, xmlinput):
        """Cuts out all the XML-tags, helper for fulltext (for content-objects)
        """
        # XXX this need to be fixed by using ZCTextIndex or the like
        return xmlinput

InitializeClass(ExampleDocumentTypeVersion)
