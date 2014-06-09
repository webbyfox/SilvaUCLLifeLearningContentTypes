## Script (Python) "get_edit_mode"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

# TODO Jon
# social_list needs to be stored in SocialComponent.py somewhere or as a service to this silva extension
# And used to generate the add form and also this.
#social_list = [('Facebook', 'facebook'), ('Twitter', 'twitter'), ('Google+', 'google')]
#format_list = [('One Column', '1'), ('Two Columns', '2'), ('Three Columns', '3')]

view = context
request = view.REQUEST
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

#social = []
#for  title, id in social_list:
#    checked = id in version.get_social() and 'true' or 'false'
#    social.append('%s|%s|%s' % (
#        entitize_and_escape_pipes(id), 
#        entitize_and_escape_pipes(title), 
#        checked)
#    )

#social = '||'.join(social)

#format = []
#for title, id in format_list:
#    checked = id in version.get_format() and 'true' or 'false'
#    format.append('%s|%s|%s' % (
#        entitize_and_escape_pipes(id), 
#        entitize_and_escape_pipes(title), 
#        checked)
#    )

#format = '||'.join(format)


meta_template = (
    '<meta scheme="http://infrae.com/namespaces/metadata/silva-news" '
    'name="%s" content="%s" />')

#metas = [
#    meta_template % ('format', format),
#    meta_template % ('social', social),
#]

metas = []

metas.append(meta_template % ('catalogue_number', version.get_catalogue_number() or ''))
metas.append(meta_template % ('catalogue_url', version.get_catalogue_url() or ''))
#metas.append(meta_template % ('height', version.get_height() or ''))
metas.append(meta_template % ('image_path', version.get_image_path() or ''))

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
