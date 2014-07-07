## Script (Python) "get_content"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=version,request
##title=
##

if version is None:
    # We can get None if there is no published version.
    return u''
request.set('suppress_title',1)
try:
    html = version.content.render()
finally:
    request.set('suppress_title',0)

for original, replace in (('<p class="p">', '<p class="quote clearfix">'),
                          ('<p class="lead">', '<p class="island greybox">')):
    html = html.replace(original, replace)
return html
