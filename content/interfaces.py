from Products.Silva.interfaces import IVersion, IContent, IVersionedContent

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
         
