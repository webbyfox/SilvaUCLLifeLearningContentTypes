##Script (Python) "add_submit_helper"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=model, id, title, result
##title=
##
model.manage_addProduct['SilvaUCLLifeLearningContentTypes'].manage_addCourseDate(id, title)
new = getattr(model, id)
#new.set_funnelback_collection(result['funnelback_collection'])
return new
