EDITABLE_METADATA = {
    'http://infrae.com/namespaces/metadata/silva-news':
    [
        {name: 'subjects', type: 'checkbox', mandatory: 0, title: 'Subjects'},
        {name: 'category', type: 'checkbox', mandatory: 0, title: 'Category'},
        {name: 'format', type: 'checkbox', mandatory: 0, title: 'Format'},
    	{name: 'shortdescription', type: 'textarea', mandatory: 0, title: 'Short description'},
        {name: 'image', type: 'reference', mandatory: 0, title: 'Image',lookup: 'Silva Image'},
        {name: 'document', type: 'reference', mandatory: 0, title: 'Document',lookup: 'Silva File'},
    ]
};
