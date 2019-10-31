from .base_error import Error # extends the 'Exception' class

class BadUrlError(Error):
    """
    Exception raised for errors in the path used to make external api calls.

    Attributes:
            url -- the path which threw the error
        message -- explanation of the error
        context -- the meta date of the function which made the server call
    """    
    def __init__(self, message, context=None, url=None):
        self.url = url
        if message is None: 
            message = "[{} {}] "+self.__class__+": {}("+url+") -- LN {}"
        super(Error, self).__init__(message, context)     
