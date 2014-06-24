#Script (Python) "render_view
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
return context.render_helper(version=context.REQUEST.model)
