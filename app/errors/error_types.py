class Error(Exception):
    """
    Base class for exceptions in this module.

    Attributes:
        context -- the meta date of the function which made the server call
    """
    def __init__(self, message = None, context = None):
        self.message = None        
        self.context = None
        self.setContext(context)
        self.setMessage(message)


    def setContext(self, context):
        def isValidContext(context):
            print('Not yet implemented')

        if isValidContext(context):
            self.context['timestamp'] = str(datetime.now or None)
            self.context['lineno'] = str(context.lineno or None)
            self.context['filename'] =str(context.filename.rpartition("/")[2].rpartition(".")[0] or None)
            self.context['function'] = str(context.function or None)
        else:
            raise AttributeError

        return self


    def setMessage(self, template):
        
        def isValidTemplate(template):
            return template.split("{}", -1).count("{}") is 4
        
        if isValidTemplate(template):
           tmplt = template 
        else:
            tmplt  = "[{}, LN {}] An error occured while executing {}::{}. "
        
        self.message = tmplt.format(
            self.context['timestamp'], 
            self.context['lineno'], 
            self.context['filename'], 
            self.context['function']
            )
        return self

class BadUrlError(Error):
    """
    Exception raised for errors in the path used to make external api calls.

    Attributes:
            url -- the path which threw the error
        message -- explanation of the error
        context -- the meta date of the function which made the server call
    """       
    def __init__(self, url, message = None, context = None):
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
    def __init__(self, api, url, message = None, context = None):
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
        