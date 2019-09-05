class Error(Exception):
    """Base class for exceptions in this module."""
    

class BadUrlError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, url, message):
        self.url = url
        self.message = message

class ApiError(Error):
    """Exception raised for errors returned when calling an A2pi.

    Attributes:
            api -- the <api> which responded with the error
            url -- the <url> used to make a call to the <api>
        message -- the error message from <api>
    """

    def __init__(self, api, url, message):
        self.api = api
        self.url = url
        self.message = message

class ServerError(Error):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        previous -- state at beginning of transition
        next -- attempted new state
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, context, message):
        self.message = message
        