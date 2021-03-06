from Products.Formulator.Errors import ValidationError, FormValidationError

# I18N stuff
from Products.Silva.i18n import translate as _

request = context.REQUEST
model = context.REQUEST.model
view = context
editable = model.get_editable()
section = editable.aq_inner.aq_parent
mypub = section.get_publication()
mypub = mypub.aq_parent.meta_type == 'Silva Publication' and mypub.aq_parent or mypub;
myid = mypub.getId()
form = view.form

try:
   result = view.form.validate_all(context.REQUEST)
except FormValidationError, e:
   return view.tab_edit(message_type="error", message=view.render_form_errors(e))


editable.set_subject(result['subject'])
editable.set_category(result['category'])
editable.set_cost(result['cost'])
editable.set_start_date(result['start_date'])
editable.set_format(result['format'])

# not sure what this line does
model.sec_update_last_author_info()

m = _('Settings changed', 'silva_news')
msg = unicode(m)

return view.tab_edit(message_type="feedback", message=msg)

