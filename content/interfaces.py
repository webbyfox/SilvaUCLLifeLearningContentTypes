from Products.Silva.interfaces import IVersion, IContent, IVersionedContent, IContainer

class ICourseDate(IContent):
    """Interface for Course Date object"""
    pass

class IReview(IContent):
     """Interface for Review object"""
     pass

class ICoursePage(IVersionedContent):
    """Interface for Course object"""
    pass   
    
class ICoursePageVersion(IVersion):
    """Interface for version of Course"""
    pass
         
class ICourse(IContainer):
	"""Interface for Course Container"""
	pass
         
class ICourseTeam(IContent):
    """Interface for Course Team"""
    pass

class ITags(IContent):
    """Interface for Tags"""
    pass
    
class IFacets(IContent):
    """Interface for Tags"""
    pass

class ICaseStudy(IVersionedContent):
    """Interface for Tags"""
    pass


class ICaseStudyVersion(IVersion):
    """Interface for Tags"""
    pass