from app.errors.myErrors.base_error import Error # extends the 'Exception' class
"""
Exception hierarchy -- The class hierarchy for built-in exceptions is:


BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
      |    +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- BlockingIOError
      |    +-- ChildProcessError
      |    +-- ConnectionError
      |    |    +-- BrokenPipeError
      |    |    +-- ConnectionAbortedError
      |    |    +-- ConnectionRefusedError
      |    |    +-- ConnectionResetError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- InterruptedError
      |    +-- IsADirectoryError
      |    +-- NotADirectoryError
      |    +-- PermissionError
      |    +-- ProcessLookupError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError
      |         +-- TabError
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning
           +-- DeprecationWarning
           +-- PendingDeprecationWarning
           +-- RuntimeWarning
           +-- SyntaxWarning
           +-- UserWarning
           +-- FutureWarning
           +-- ImportWarning
           +-- UnicodeWarning
           +-- BytesWarning
           +-- ResourceWarning
"""

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

class ArithmeticOperationError(Error):
    """
    Raised when an operation attempts a state transition that's not allowed.

    Attributes:
        message -- explanation of the error
        context -- the meta data of the function which made the server call
    """
    def __init__(self, message, context=None, params=None):
        if message is None: 
            if params and set(("input_1", "input_2")) <= set(dir(params)):
                self.params = params
                message = "[{} {}] "+self.__class__+": "+params["input_1"]+".{}("+params["input_2"]+") -- LN {}"
            elif params is None:
                message = "[{} {}] "+self.__class__+": <Unknown>.{}(<Unknown>) -- LN {}"

        super(Error, self).__init__(message, context)   

class TypeMatchError(Error):
    """
    Raised when an operation fails due to it being performed on incompatible types

    Attributes:
        message -- explanation of the error
        context -- the meta data of the function which made the server call
    """
    def __init__ (self, message, context=None, params=None):
        if message is None:
            if params and set(("input_1", "input_2")) <= set(dir(params)):
                self.params = params
                message = "[{} {}] "+self.__class__+": "+params["input_1"]+".{}("+params["input_2"]+") -- LN {}"
            elif params is None:
                message = "[{} {}] "+self.__class__+": <Unknown>.{}(<Unknown>) -- LN {}"

        super(Error, self).__init__(message, context)

class InternalServerError(Error):
    """
    Raised when an operation attempts a state transition that's not allowed.

    Attributes:
        message -- explanation of the error
        context -- the meta date of the function which made the server call
    """
    def __init__(self, message=None, context=None):
        super().__init__(message, context)   


  