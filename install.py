"""Install for SilvaUCLLifeLearningContentTypes
"""
from os import path
from Globals import package_home 

from Products.Silva.install import add_fss_directory_view
from Products.Silva import roleinfo
from Products.SilvaMetadata.Extensions.SilvaInstall import install as install_metadata

metadatasets = []


def install(root):
    # create the core views from filesystem
    add_fss_directory_view(root.service_views, 'SilvaUCLLifeLearningContentTypes', __file__, 'views')

    # also register views
    registerViews(root.service_view_registry)

    # metadata
    setupMetadata(root)

    # security
    configureSecurity(root)

def configureSecurity(root):
    all_author = [ 'Author', 'Editor', 'ChiefEditor', 'Manager']
    
    add_permissions = [
        'Add Course Dates', 
        'Add Reviews',
#        'Add Courses',
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
            {'type': 'Course Date', 'chain': 'silva-content , silva-extra'},
            {'type': 'Review', 'chain': 'silva-content , silva-extra'},
 #           {'type': 'Course', 'chain': 'silva-content , silva-extra'},
        )

    mapping.editMappings(default, tm)
    root.service_metadata.initializeMetadata()


def uninstall(root):
    """unregister views for product"""
    unregisterViews(root.service_view_registry)
    root.service_views.manage_delObjects(['SilvaUCLLifeLearningContentTypes'])

def is_installed(root):
    """Test is uninstalled"""
    return hasattr(root.service_views, 'SilvaUCLLifeLearningContentTypes')

def registerViews(reg):
    """Register core views on registry.
    """
    # Couse date views
    reg.register('add', 'Course Date', ['add', 'CourseDate'])
    reg.register('edit','Course Date', ['edit', 'Content','CourseDate'])
    reg.register('public', 'Course Date', ['public', 'CourseDate'])
    reg.register('preview', 'Course Date', ['public','CourseDate','preview'])

    # Review views
    reg.register('add', 'Review', ['add', 'Review'])
    reg.register('edit','Review', ['edit', 'Content','Review'])
    reg.register('public', 'Review', ['public', 'Review'])
    reg.register('preview', 'Review', ['public','Review','preview'])

    # Course item
#    reg.register('add', 'Course', ['add', 'Course'])
#    reg.register('edit','Course', ['edit', 'Content','Course'])
#    reg.register('public', 'Course', ['public', 'Course'])
#    reg.register('preview', 'Course', ['public','Course','preview'])



def unregisterViews(reg):
    """unregister all the views"""
    for meta_type in ['Course Date',
                      'Review',
            #          'Course,'
                     ]:
        reg.unregister('edit', meta_type)
        reg.unregister('public', meta_type)
        reg.unregister('add', meta_type)
        reg.unregister('preview', meta_type)
