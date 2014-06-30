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
    """Interface for Facets"""
    pass

class ICaseStudy(IVersionedContent):
    """Interface for Case Study"""
    pass


class ICaseStudyVersion(IVersion):
    """Interface for Case study version"""
    pass

class ICourseSubject(IVersionedContent):
    """Interface for Course Subject Page"""
    pass


class ICourseSubjectVersion(IVersion):
    """Interface for Course Subject Page version"""
    pass