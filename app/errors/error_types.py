class Error(Exception):
    """
    Base class for exceptions in this module.

    Attributes:
        context -- the meta date of the function which made the server call
    """
    def __init__(self, context, *args, **kwargs):
        self.context = context

class BadUrlError(Error):
    """
    Exception raised for errors in the path used to make external api calls.

    Attributes:
            url -- the path which threw the error
        message -- explanation of the error
        context -- the meta date of the function which made the server call
    """
        
    def __init__(self, url, message, context = None):
        self.url = url
        self.message = message
        if not context is None:
            super().__init__(context)
        

class ApiError(Error):
    """
    Exception raised for errors returned when calling an external Api.

    Attributes:
            api -- the <api> which responded with the error
            url -- the <url> used to make a call to the <api>
        message -- the error <message> from <api>
        context -- the meta date of the function which made the server call
    """
    def __init__(self, api, url, message, context = None):
        self.api = api
        self.url = url
        self.message = message
        if not context is None:
            super().__init__(context)

class ServerError(Error):
    """
    Raised when an operation attempts a state transition that's not allowed.

    Attributes:
        message -- explanation of the error
        context -- the meta date of the function which made the server call
    """
    def __init__(self, message, context = None):
        self.message = message
        if not context is None:
            super().__init__(context)
        