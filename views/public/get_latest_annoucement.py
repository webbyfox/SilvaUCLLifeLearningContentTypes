anouncement_items = []
for item in  context.service_catalog(meta_type={'query':'Anouncement Version},
                                     path={'query' : '/Silva/life-learning', 'depth' :0},
                                     version_status = 'public')[:3]:
    
     anouncement_items.append([item.get_title[0:75], item.getURL()])

return anouncement_items
