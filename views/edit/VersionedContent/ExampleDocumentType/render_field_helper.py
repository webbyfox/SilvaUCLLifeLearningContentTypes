## Script (Python) "render_field_helper"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=field
##title=
##

"""Takes care of some irregular fields and stickyness of the form"""

request = context.REQUEST
model = request.model
editable = model.get_editable()

value = ''
reqvalue = request.get('field_%s' % field.id)
if reqvalue is not None:
    value = unicode(reqvalue, 'UTF-8')
elif field.id == 'object_title':
    value = editable.get_title()
else:
    value = getattr(editable, field.id)()

return field.render(value)
