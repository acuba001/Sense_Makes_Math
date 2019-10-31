from .base_error import Error # extends the 'Exception' class

class InternalServerError(Error):
    """
    Raised when an operation attempts a state transition that's not allowed.

    Attributes:
        message -- explanation of the error
        context -- the meta date of the function which made the server call
    """
    def __init__(self, message=None, context=None):
        super().__init__(message, context)   
