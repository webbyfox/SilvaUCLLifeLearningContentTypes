## Script (Python) "get_tabs"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# define:
# name, id/None, up_id, toplink_accesskey, tab_accesskey, uplink_accesskey
from Products.Silva.i18n import translate as _

tabs = [('edit', 'tab_edit', 'tab_edit', '!', '1', '6'),
        ('preview', 'tab_preview', 'tab_preview', '@', '2', '7'),
        ('properties', 'tab_metadata', 'tab_metadata', '#', '3', '8'),
        ('access', 'tab_access', 'tab_access', '$', '4', '9'),
        ('publish', 'tab_status', 'tab_status', '%', '5', '0'),
       ]

return tabs
