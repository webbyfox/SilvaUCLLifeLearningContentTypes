EDITABLE_METADATA = {
    'http://infrae.com/namespaces/metadata/silva-news':
    [
    	{name: 'shortdescription', type: 'textarea', mandatory: 0, title: 'Short description'},
    	{name: 'url', type: 'text', mandatory: 0, title: 'URL'},
        {name: 'image', type: 'reference', mandatory: 0, title: 'Image',lookup: 'Silva Image'},
        {name: 'document', type: 'reference', mandatory: 0, title: 'Document',lookup: 'Silva File'},
    ]
};
