##Script (Python) "add_submit_helper"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=model, id, title, result
##title=
##
model.manage_addProduct['SilvaUCLLifeLearningContentTypes'].manage_addCoursePage(id, title)
coursepage = getattr(model, id)
version = coursepage.get_editable()
version.set_subjects(result['subjects'])
version.set_category(result['category'])
version.set_format(result['format'])

return coursepage
