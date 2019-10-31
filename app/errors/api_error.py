from .base_error import Error # extends the 'Exception' class

class BadApiCallError(Error):
    """
    Exception raised for errors returned when calling an external Api.

    Attributes:
            api -- the <api> which responded with the error
            url -- the <url> used to make a call to the <api>
        message -- the error <message> from <api>
        context -- the meta date of the function which made the server call
    """
    def __init__(self, message, context=None, api=None, url=None):
        self.type = str(self.__class__).split(".").pop()
        self.api = str(api)
        self.url = str(url)
        if message is None:
            error_type = self.type.split(">")[0]
            message = "[{} {}] "+error_type+": {}.{}("+self.url+")"
        super().__init__(message, context)   
