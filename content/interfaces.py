from Products.Silva.interfaces import IVersionedContent, IVersion, IContainer

class IExampleDocumentType(IVersionedContent):
	"""interface for ExampleDocumentType"""

class IExampleDocumentTypeVersion(IVersion):
	"""interface for version of an ExampleDocumentType"""

class IExampleFolderType(IContainer):
	"""interface for ExampleFolderType"""

