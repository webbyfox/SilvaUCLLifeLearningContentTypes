##parameters=publish_now
from Products.Silva.i18n import translate as _
from Products.Formulator.Errors import ValidationError, FormValidationError
from DateTime import DateTime

model = context.REQUEST.model
view = context

if not model.get_unapproved_version():
    # SHORTCUT: To allow approval of closed docs with no new version available,
    # first create a new version. This "shortcuts" the workflow.
    # See also edit/Container/tab_status_approve.py
    if model.is_version_published():
        if publish_now:
            message=_("There is no unapproved version to publish.")
        else:
            message=_("There is no unapproved version to approve.")
            
        return view.tab_status(
            message_type="error", 
            message=message)
    model.create_copy()

try:
    result = view.tab_status_form_editor.validate_all(context.REQUEST)
except FormValidationError, e:
    return view.tab_status(
        message_type="error", message=view.render_form_errors(e))

try:
    result_news_form = view.tab_status_form_news.validate_all(context.REQUEST)
except FormValidationError, e:
    # highly unlikely
    return view.tab_status(message_type='error', 
                                message='Error in display datetime fields')

unapproved = getattr(model, model.get_unapproved_version())

now = DateTime()
if publish_now:
    pdt = now
else:
    pdt = result['publish_datetime']
    
# set display datetime
ddt = result_news_form['display_datetime']
if ddt is None:
    ddt = pdt
elif pdt > now and unapproved.display_datetime() == ddt:
    # bug 101729: if ddt is set and unchanged,
    #             and publication time is in the future,
    #             set ddt to the future publication time.
    ddt = pdt

unapproved.set_display_datetime(ddt)
    
model.set_unapproved_version_publication_datetime(pdt)

expiration = result['expiration_datetime']
if expiration:
    model.set_unapproved_version_expiration_datetime(expiration)

model.approve_version()

if hasattr(model, 'service_messages'):
    model.service_messages.send_pending_messages()

if publish_now:
    message = _("Version published.")
else:
    message = _("Version approved.")
    
return view.tab_status(message_type="feedback", message=message)

