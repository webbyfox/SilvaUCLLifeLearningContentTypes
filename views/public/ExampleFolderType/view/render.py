## Script (Python) "render"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
return context.render_index()

#request = context.REQUEST
#model = request.model
#default = model.get_default() or None

#if default is None:
#    return ''

#return default.view()
