# Copyright (c) 2014 University College London. All rights reserved.

# Zope
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from zope.interface import implements

# Silva
from Products.Silva import SilvaPermissions
from Products.Silva.interfaces import IContainer
from Products.Silva.Folder import Folder

from interfaces import ICourse


class Course(Folder):
	"""
	Course container object
	"""
	implements(ICourse)
	meta_type = "Course"
	security = ClassSecurityInfo()

	def __init__(self, id):
		
		Course.inheritedAttribute('__init__')(self, id)
		
		self._subjects = ""
		self._category = ""
		self._format = ""

	security.declareProtected(SilvaPermissions.AccessContentsInformation, 'get_components')
	def get_components(self):
		filtered_items = list(self.filter_entries(self.get_orderded_publishables()))
		return filtered_items

	# Mutator
	def set_subjects(self, subjects):
		self._subjects  = subjects 

	# Accessor
	def get_subjects(self):
		if not hasattr(self, '_subjects'):
			self._subjects  = ""
		else:
			return self._subjects

	# Mutator
	def set_category(self,category):
		self._category = category

	# Accessor
	def get_category(self):
		if not hasattr(self, '_category'):
			self._category = ""
		else:
			return self._category

	# Mutator
	def set_format(self,format):
		self._format = format

	# Accessor
	def get_format(self):
		if not hasattr(self, '_format'):
			self._format = ""
		else:
			return self._format

InitializeClass(Course)

def course_added(course, event):
	"""
	Event Handler:	While course container added, it adds course page, and some SilvaDocuments
	"""
	if event.oldParent is None and event.object == course:
		if course.get_default() is None:
			factory = course.manage_addProduct['SilvaUCLLifeLearningContentTypes']
			factory.manage_addCoursePage('index', 'Index')
        
        ids = course.objectIds()
        if 'learning-outcomes' not in ids:
        	factory = course.manage_addProduct['SilvaDocument']
        	factory.manage_addDocument('learning-outcomes', 'Learning Outcomes')
		
		if 'faq' not in ids:
			factory = course.manage_addProduct['SilvaDocument']
			factory.manage_addDocument('faq', 'FAQs')