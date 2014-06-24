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
        'Add Course Pages',
        'Add Course Page Versions',
        'Add Courses',
        'Add Course Teams',
        'Add Course Tagss',
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
            {'type': 'Course', 'chain': 'silva-content , silva-extra'},
            {'type': 'Course Page Version', 'chain': 'silva-content , silva-extra'},
            {'type': 'Course Team', 'chain': 'silva-content , silva-extra'},
            {'type': 'Course Tags', 'chain': 'silva-content , silva-extra'},
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
    reg.register('public', 'Course Date', ['public', 'CourseDate', 'view'])
    reg.register('preview', 'Course Date', ['public','CourseDate','preview'])

    # Review views
    reg.register('add', 'Review', ['add', 'Review'])
    reg.register('edit','Review', ['edit', 'Content','Review'])
    reg.register('public', 'Review', ['public', 'Review', 'view'])
    reg.register('preview', 'Review', ['public','Review','preview'])

    # Course Page item
    reg.register('add', 'Course Page', ['add', 'CoursePage'])
    reg.register('edit','Course Page', ['edit', 'VersionedContent','CoursePage'])
    reg.register('public', 'Course Page', ['public', 'CoursePage', 'view'])
    reg.register('public', 'Course Page Version', ['public', 'CoursePage', 'view'])
    reg.register('preview', 'Course Page Version', ['public','CoursePage','preview'])

    # Course container
    reg.register('add', 'Course', ['add', 'Course'])
    reg.register('edit','Course', ['edit', 'Container','Course'])
    reg.register('public', 'Course', ['public', 'Course', 'view'])
    reg.register('public', 'Course', ['public', 'Course', 'view'])
    reg.register('preview', 'Course', ['public','Course','preview'])

    # Course Team view registry
    reg.register('add', 'Course Team', ['add', 'CourseTeam'])
    reg.register('edit','Course Team', ['edit', 'Content','CourseTeam'])
    reg.register('public', 'Course Team', ['public', 'CourseTeam', 'view'])
    reg.register('preview', 'Course Team', ['public','CourseTeam','preview'])

    # Tags view registry
    reg.register('add', 'Course Tags', ['add', 'Tags'])
    reg.register('edit','Course Tags', ['edit', 'Content','Tags'])
    reg.register('public', 'Course Tags', ['public', 'Tags', 'view'])
    reg.register('preview', 'Course Tags', ['public','Tags','preview'])


def unregisterViews(reg):
    """unregister all the views"""
    for meta_type in [
                      'Course Date',
                      'Review',
                      'Course',
                      'Course Team',
                      'Course Tags'
                      
                     ]:
        reg.unregister('edit', meta_type)
        reg.unregister('public', meta_type)
        reg.unregister('add', meta_type)
        reg.unregister('preview', meta_type)
    for meta_type in ['Course Page',]:
        reg.unregister('edit', meta_type)
        reg.unregister('add', meta_type)
        reg.unregister('public', meta_type)
        reg.unregister('public', '%s Version' % meta_type)
        reg.unregister('preview', '%s Version' % meta_type)