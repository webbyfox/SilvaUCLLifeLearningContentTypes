# Copyright (c) 2002-2008 Infrae. All rights reserved.
# See also LICENSE.txt
# $Revision: 1.25 $

from StringIO import StringIO
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from Products.Silva.helpers import translateCdata
from Products.Silva.Metadata import export_metadata
from Products.ParsedXML.ParsedXML import ParsedXML
from Products.Silva import SilvaPermissions
from Products.Silva.i18n import translate as _

from Products.SilvaDocument.transform.Transformer import EditorTransformer
from Products.SilvaDocument.transform.base import Context

from Products.Silva.adapters.renderable import getRenderableAdapter

class SilvaXMLAttribute(SimpleItem):
    """An attribute that contains Silva XML"""

    security = ClassSecurityInfo()
    meta_type = 'Silva XML Attribute'

    def __init__(self, id):
        self.id = id
        self._content = ParsedXML(id, '<doc></doc>')

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                                'get_content')
    def get_content(self):
        """need a way to retrieve xml content from untrusted code"""
        return self._content

    security.declareProtected(SilvaPermissions.AccessContentsInformation, 
                                'toXML')
    def toXML(self, out):
        """returns contents of this field, serialized as XML"""
        out.write('<%s type="xml">' % self.id)
        self._content.documentElement.writeStream(out)
        out.write('</%s>' % self.id)

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                                'render')
    def render(self):
        """return the rendered contents"""
        docel = self._content.documentElement
        service_editor = self.service_editor
        service_editor.setViewer('service_doc_viewer')
        return service_editor.renderView(docel)

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                                'editorHTML')
    def editorHTML(self, editor='kupu', encoding=None):
        """returns the HTML for a ParsedXML field"""
        s = StringIO()
        contents = self.toXML(s)
        return self._transformSLVToHTML(s.getvalue(), editor, encoding)

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
                                'saveEditorHTML')
    def saveEditorHTML(self, html, editor='kupu', encoding=None):
        """saves the HTML to a ParsedXML field"""
        title, xml = self._transformHTMLToSLV(html, editor, encoding)
        self._content.manage_edit(xml)

    def clearEditorCache(self):
        """ Clears editor cache for this version
        """
        editor_service = self.service_editor
        document_element = self._content.documentElement
        editor_service.clearCache(document_element)

    def isCachable(self):
        """Return true if this document is cacheable.
        That means the document contains no dynamic elements like
        code, datasource or toc.
        """
        non_cacheable_elements = ['toc', 'code',]
        # It should suffice to test the children of the root element only,
        # since currently the only non-cacheable elements are root elements
        # XXX Are we very sure it isn't possible to add code elements and tocs
        # inside tables or lists?
        for node in self._content.documentElement.childNodes:
            node_name = node.nodeName
            if node_name in non_cacheable_elements:
                return False
            # FIXME: how can we make this more generic as it is very
            # specific now..?
            if node_name == 'source':
                if not externalsource.isSourceCachable(self.aq_inner, 
                        node):
                    return False
        return True

    def fulltext(self):
        """Returns the text of all text nodes as a flat string"""
        return self._fulltext_helper(self._content.documentElement)

    def _fulltext_helper(self, node):
        ret = []
        for child in node.childNodes:
            if child.nodeType == child.TEXT_NODE:
                ret.append(child.nodeValue)
            elif child.nodeType == child.ELEMENT_NODE:
                ret.append(self._fulltext_helper(child))
        return ' '.join(ret)
        
    def _transformSLVToHTML(self, string, editor='kupu', encoding=None):
        """transform Silva XML to HTML"""
        transformer = EditorTransformer(editor=editor)

        # we need to know what browser we are dealing with in order to know
        # what html to produce, unfortunately Mozilla uses different tags in
        # some cases (b instead of strong, i instead of em)
        browser = 'Mozilla'
        if self.REQUEST['HTTP_USER_AGENT'].find('MSIE') > -1:
            browser = 'IE'

        ctx = Context(f=StringIO(),
                        last_version=1,
                        url=self.aq_parent.absolute_url(),
                        browser=browser,
                        model=self.aq_parent)
        ctx.f.write(string)

        htmlnode = transformer.to_target(sourceobj=ctx.f.getvalue(), 
                                            context=ctx)
        if encoding is not None:
            ret = htmlnode.asBytes(encoding=encoding)
            ret = ret.replace('\xa0', '&nbsp;')
        else:
            ret = unicode(htmlnode.asBytes('utf8'),'utf8')
            ret = ret.replace(u'\xa0', u'&nbsp;')

        return ret

    def _transformHTMLToSLV(self, string, editor='kupu', encoding=None):
        """transform (messy structure-wise) HTML to Silva XML"""
        transformer = EditorTransformer(editor=editor)

        # we need to know what browser we are dealing with in order to know
        # what html to produce, unfortunately Mozilla uses different tags in
        # some cases (b instead of strong, i instead of em)
        browser = 'Mozilla'
        if self.REQUEST['HTTP_USER_AGENT'].find('MSIE') > -1:
            browser = 'IE'

        ctx = Context(url=self.aq_parent.absolute_url(),
                        browser=browser,
                        model=self.aq_parent,
                        request=self.REQUEST)
        silvanode = transformer.to_source(targetobj=string, context=ctx)[0]

        title = silvanode.find('title')[0].extract_text() # unicode
        docnode = silvanode.find('doc')[0]
        content = docnode.asBytes(encoding="UTF8") # UTF-8

        return title, content

InitializeClass(SilvaXMLAttribute)
