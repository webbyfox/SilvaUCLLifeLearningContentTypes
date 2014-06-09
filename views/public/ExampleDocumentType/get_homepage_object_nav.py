## Script (Python) "get_homepage_object_nav"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##


zc = context.service_catalog
indexitems = zc.searchResults({'meta_type':'ThreeD Object Index'})
url = '#'
if indexitems:
    obj = indexitems[0].getObject()
    url = obj.absolute_url()
#    url = indexitems[0].silva_object_url
return url