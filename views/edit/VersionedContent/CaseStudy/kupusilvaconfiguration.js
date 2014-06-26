EDITABLE_METADATA = {
    'http://infrae.com/namespaces/metadata/silva-news':
    [
    	{name: 'pagetitle', type: 'text', mandatory: 0, title: 'Page Title'},
    	{name: 'shortdescription', type: 'textarea', mandatory: 0, title: 'Short description'},
        {name: 'image', type: 'reference', mandatory: 0, title: 'Image',lookup: 'Silva Image'},
        {name: 'document', type: 'reference', mandatory: 0, title: 'Document',lookup: 'Silva File'},
    ]
};
