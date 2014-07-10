EDITABLE_METADATA = {
    'http://infrae.com/namespaces/metadata/silva-news':
    [
    	{name: 'shortdescription', type: 'textarea', mandatory: 0, title: 'Short description'},
    	{name: 'adminname', type: 'text', mandatory: 0, title: 'Admin Name'},
    	{name: 'adminemail', type: 'text', mandatory: 0, title: 'Admin Email'},
    	{name: 'admintelephone', type: 'text', mandatory: 0, title: 'Admin Telephone'},
    	{name: 'timingaccess', type: 'text', mandatory: 0, title: 'Timing Access'},
    	{name: 'location', type: 'text', mandatory: 0, title: 'Location'},
    	{name: 'locationurl', type: 'text', mandatory: 0, title: 'Location URL'},
        {name: 'partnerimage1', type: 'reference', mandatory: 0, title: 'Partner Image 1',lookup: 'Silva Image'},
        {name: 'partnerimage2', type: 'reference', mandatory: 0, title: 'Partner Image 2',lookup: 'Silva Image'},
        {name: 'partnerimage3', type: 'reference', mandatory: 0, title: 'Partner Image 3',lookup: 'Silva Image'},
        {name: 'cost', type: 'text', mandatory: 0, title: 'Cost'},
    	{name: 'learninghours', type: 'text', mandatory: 0, title: 'Learning Hours'},
    	{name: 'courseduration', type: 'text', mandatory: 0, title: 'Course Duration'},
        {name: 'subjects', type: 'checkbox', mandatory: 0, title: 'Subjects'},
        {name: 'category', type: 'checkbox', mandatory: 0, title: 'Category'},
        {name: 'format', type: 'checkbox', mandatory: 0, title: 'Format'},
    		
    ]
};
