from datetime import datetime
class Error(Exception):
    """
    Base class for exceptions in this module.

    Attributes:
        context -- the meta date of the function which made the server call
    """
    def __init__(self, message, context = None):
        self.message = message        
        self.context = setContext(context)

    def setContext(self, context):
        if not context is None:
            self.context['timestamp'] = str(datetime.now or None)
            self.context['lineno'] = str(context.lineno or None)
            self.context['filename'] =str(context.filename.rpartition("/")[2].rpartition(".")[0] or None)
            self.context['function'] = str(context.function or None)
        return self

    def setMessage(self, message):
        err_message = None
        template = "[{} , LN {}] An error occured while executing {}::{}. "
        err_message = template.format(
            self.context['timestamp'], 
            self.context['lineno'], 
            self.context['filename'], 
            self.context['function']
            )
        self.response['error'] = err_message
        return self

class BadUrlError(Error):
    """
    Exception raised for errors in the path used to make external api calls.

    Attributes:
            url -- the path which threw the error
        message -- explanation of the error
        context -- the meta date of the function which made the server call
    """       
    def __init__(self, url, message, context):
        self.url = url
        super().__init__(message, context)
        

class ExternalServerError(Error):
    """
    Exception raised for errors returned when calling an external Api.

    Attributes:
            api -- the <api> which responded with the error
            url -- the <url> used to make a call to the <api>
        message -- the error <message> from <api>
        context -- the meta date of the function which made the server call
    """
    def __init__(self, api, url, message, context):
        self.api = api
        self.url = url
        super().__init__(message, context)

class InternalServerError(Error):
    """
    Raised when an operation attempts a state transition that's not allowed.

    Attributes:
        message -- explanation of the error
        context -- the meta date of the function which made the server call
    """
    def __init__(self, message, context):
        super().__init__(message, context)
        