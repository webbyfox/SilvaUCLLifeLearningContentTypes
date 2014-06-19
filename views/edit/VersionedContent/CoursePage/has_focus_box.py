## Script (Python) "has_focus_box"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=tab_id
##title=
##
return 0

if not tab_id == 'tab_edit':
    return 0
model = context.REQUEST.model
version = model.get_unapproved_version()
if version is None:
    return 0
version = getattr(model, version)
content_widget_path = context.service_simple_editor.getNodeWidgetFinder().getWidget(version.content)

if content_widget_path and content_widget_path[-1] == 'mode_edit':
    return 1
return 0
