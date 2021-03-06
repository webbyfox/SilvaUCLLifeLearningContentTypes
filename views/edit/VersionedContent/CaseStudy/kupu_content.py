## Script (Python) "get_edit_mode"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
request = context.REQUEST
model = request.model
version = model.get_editable()

def entitize_and_escape_pipes(str):
    """Escapes all XML entities in str and escapes all pipes.

        This is done so the str can be used as the value of a pipe-seperated
        string, which is used as the value of a metadata tag (to be used by
        Kupu's SilvaPropertyTool later on).

        Escaping of a pipe happens with an invented entity '&pipe;'.
    """
    str = str.replace('&', '&amp;')
    str = str.replace('"', '&quot;')
    str = str.replace('<', '&lt;')
    str = str.replace('>', '&gt;')
    str = str.replace('|', '&pipe;')
    return str

response = request.RESPONSE
headers = [('Expires', 'Mon, 26 Jul 1997 05:00:00 GMT'),
           ('Last-Modified',
            DateTime("GMT").strftime("%a, %d %b %Y %H:%M:%S GMT")),
           ('Cache-Control', 'no-cache, must-revalidate'),
           ('Cache-Control', 'post-check=0, pre-check=0'),
           ('Pragma', 'no-cache'),
]

placed = []
for key, value in headers:
    if key not in placed:
        response.setHeader(key, value)
        placed.append(key)
    else:
        response.addHeader(key, value)

response.setHeader('Content-Type', 'text/html;charset=utf-8')

docref = model.create_ref(model)
doctitle = version.get_title()
xhtml = version.content.editorHTML()

# gather metadata
meta_template = (
    '<meta scheme="http://infrae.com/namespaces/metadata/silva-news" '
    'name="%s" content="%s" />')

subjects_list = ['Art and Humanities', 'Built Environment', 'Business, Policy, Leadership and Management', 'Engineering and Technology', 'Education', 'Languages','Law, Crime and Security', 'Healthcare, Medical and Life Sciences', 'Mathematical, Physical and Natural Sciences', 'Social and Historical Sciences', ]
category_list = ['Executive Eductation',  'Professional Development', 'Recreational Development', 'Summer Schools',]
format_list = ['Online learning', 'Face to Face learning', 'Blended learning',]

subjects = []
for id in subjects_list:
    checked = id in version.get_subjects() and 'true' or 'false'
    subjects.append('%s|%s|%s' % (
        entitize_and_escape_pipes(id),
        entitize_and_escape_pipes(id),
        checked)
    )

category = []
for id in category_list:
    checked = id in version.get_category() and 'true' or 'false'
    category.append('%s|%s|%s' % (
        entitize_and_escape_pipes(id),
        entitize_and_escape_pipes(id),
        checked)
    )

format = []
for id in format_list:
    checked = id in version.get_format() and 'true' or 'false'
    format.append('%s|%s|%s' % (
        entitize_and_escape_pipes(id),
        entitize_and_escape_pipes(id),
        checked)
    )

subjects = '||'.join(subjects)
category = '||'.join(category)
format = '||'.join(format)

metas = [
    meta_template % ('subjects', subjects),
    meta_template % ('category', category),
    meta_template % ('format', format),
]


if hasattr(version, 'get_shortdescription'):
    metas.append(meta_template % ('shortdescription', version.get_shortdescription() or ''))

if hasattr(version, 'get_image'):
    metas.append(meta_template % ('image', version.get_image() or ''))

if hasattr(version, 'get_document'):
    metas.append(meta_template % ('document', version.get_document() or ''))


return ('<html>\n'
        '<head>\n'
        '<title>%s</title>\n'
        '<link href="%s" type="text/css" rel="stylesheet" />\n'
        '<link href="%s" type="text/css" rel="stylesheet" />\n'
        '%s\n'
        '<meta http-equiv="Content-Type" '
        'content="text/html; charset=UTF-8" />\n'
        '<meta name="docref" content="%s" />\n'
        '</head>\n'
        '<body>\n'
        '<h2>%s</h2>\n'
        '%s\n'
        '</body>\n'
        '</html>' % (doctitle,
                     getattr(context.globals, 'frontend.css').absolute_url(),
                     getattr(context.globals, 'kupu.css').absolute_url(),
                     '\n'.join(metas),
                     docref,
                     doctitle,
                     xhtml))
