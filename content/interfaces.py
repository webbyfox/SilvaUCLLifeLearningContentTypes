from Products.Silva.interfaces import IVersionedContent, IVersion, IContainer, IContent, IVersionedContent

class ICourseDate(IContent):
    """Interface for Course Date object"""
    pass

class IReview(IContent):
     """Interface for Review object"""
     pass

class ICourse(IVersionedContent):
    """Interface for Course object"""
    pass   
    
class ICourseVersion(IVersion):
    """Interface for version of Course"""
    pass
         
