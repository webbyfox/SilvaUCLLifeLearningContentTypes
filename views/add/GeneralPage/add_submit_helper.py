##Script (Python) "add_submit_helper"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=model, id, title, result
##title=
##
model.manage_addProduct['SilvaUCLLifeLearningContentTypes'].manage_addGeneralPage(id, title)
page = getattr(model, id)
version = page.get_editable()
#version.set_pagetitle(result['pagetitle'])
#version.set_shortdescription(result['ShortDescription'])
#version.set_adminname(result['AdminName'])
# more to follow
return page
