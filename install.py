"""Install for SilvaUCLExampleContentTypes
"""
from os import path
from Globals import package_home

from Products.Silva.install import add_fss_directory_view
from Products.Silva import roleinfo
from Products.SilvaMetadata.Extensions.SilvaInstall import install as install_metadata

metadatasets = []


def install(root):
    # create the core views from filesystem
    add_fss_directory_view(root.service_views, 'SilvaUCLExampleContentTypes', __file__, 'views')

    # also register views
    registerViews(root.service_view_registry)

    # metadata
    setupMetadata(root)

    # security
    configureSecurity(root)

    # addables
#    configureAddables(root)

def configureSecurity(root):
    all_author = ['ChiefEditor', 'Manager']
    
    add_permissions = [
        'Add Example Folders',
        'Add Example Documents',
        'Add Example Document Versions',
        ]

    for perm in add_permissions:
        root.manage_permission(perm, all_author)

def setupMetadata(root):
    product = package_home(globals())
    schema = path.join(product, 'schema')

    for setid, xmlfilename, types in metadatasets:
        collection = root.service_metadata.getCollection()
        if not setid in collection.objectIds():
            xmlfile = path.join(schema, xmlfilename)
            definition = open(xmlfile, 'r')
            collection.importSet(definition)


    mapping = root.service_metadata.getTypeMapping()
    default = ''
    tm = (
            {'type': 'Example Folder', 'chain': 'silva-content, silva-extra, silva-layout'},
            {'type': 'Example Document', 'chain': 'silva-content, silva-extra'},
            {'type': 'Example Document Version', 'chain': 'silva-content, silva-extra'},
        )

    mapping.editMappings(default, tm)
    root.service_metadata.initializeMetadata()

# BEN NOT USED - DELETE IF OKAY
def configureAddables(root):
    """Make sure the components aren't addable in the root but the homepages are"""
# this is not necessary if you want your content types to be added anywhere.
    news_non_addables = ['Example Document']
    news_addables = ['Example Folder']
    current_addables = root.get_silva_addables_allowed_in_publication()
    new_addables = []
    for a in current_addables:
        if a not in news_non_addables:
            new_addables.append(a)
    for a in news_addables:
        if a not in new_addables:
            new_addables.append(a)
    root.set_silva_addables_allowed_in_publication(new_addables)

def uninstall(root):
    """unregister views for product"""
    unregisterViews(root.service_view_registry)
    root.service_views.manage_delObjects(['SilvaUCLExampleContentTypes'])

def is_installed(root):
    """Test is uninstalled"""
    return hasattr(root.service_views, 'SilvaUCLExampleContentTypes')

def registerViews(reg):
    """Register core views on registry.
    """
    # edit
    reg.register('edit', 'Example Folder', ['edit', 'Container', 'Folder', 'ExampleFolderType'])
    reg.register('edit', 'Example Document', ['edit','VersionedContent','ExampleDocumentType'])

    # public
    reg.register('public', 'Example Folder', ['public', 'ExampleFolderType','view'])
    reg.register('public', 'Example Document Version', ['public','ExampleDocumentType','view'])
    reg.register('public', 'Example Document', ['public','ExampleDocumentType','view'])

    #preview
    reg.register('preview', 'Example Folder', ['public', 'ExampleFolderType','preview'])
    reg.register('preview', 'Example Document Version', ['public','ExampleDocumentType','preview'])

    # add
    reg.register('add', 'Example Folder', ['add', 'ExampleFolderType'])
    reg.register('add', 'Example Document', ['add', 'ExampleDocumentType'])


def unregisterViews(reg):
    """unregister all the views"""
    for meta_type in ['Example Folder']:
        reg.unregister('edit', meta_type)
        reg.unregister('public', meta_type)
        reg.unregister('add', meta_type)
        reg.unregister('preview', meta_type)
    # versioned objects
    for meta_type in ['Example Document']:
        reg.unregister('edit', meta_type)
        reg.unregister('add', meta_type)
        reg.unregister('public', meta_type)
        reg.unregister('public', '%s Version' % meta_type)
        reg.unregister('preview', '%s Version' % meta_type)