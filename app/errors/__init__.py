from flask import Blueprint
errors_bp = Blueprint('errors', __name__)

from datetime import datetime


class Error(Exception):
    """
    Base class for exceptions in this project.
    Exception hierarchy -- The class hierarchy for built-in exceptions is:

    Attributes:
        template -- the template of the message to be set.
        context -- the meta data of the function which made the server call

            {
                'timestamp': datetime.now(),
                'lineno': -1,
                'filename': self.__context__,
                'function': self.__traceback__,
                ...
            }
    Methods:
        None

    Hierarchy of Python3 Exception Classes:
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
    def __init__(self, template, context=None):

        # Validate Context
        def isValidContext(context):
            isNotNone = context is not None
            print("Is Context Not None: "+str(isNotNone))

            isGoodType = type(context) is type({})
            print("Is Context Good Type: "+str(isGoodType))

            isNotEmpty = context is not {}
            print("Is Context Not Empty: "+str(isNotEmpty))

            isValidFields = set(("lineno", "filename", "function")) <= set(dir(context))
            print("Is Context Valid Fields: "+str(isValidFields))

            return isNotNone and isGoodType and isNotEmpty# and isValidFields

        # Configure Context
        if isValidContext(context):
            self.context = {
                'timestamp': datetime.now(),
                'lineno': context['lineno'],
                'filename': context['filename'].rpartition("/")[2].rpartition(".")[0],
                'function': context['function']
            }
        else:
            self.context = {
                'timestamp': datetime.now(),
                'lineno': str(-1),
                'filename': '<Unknown>',
                'function': '<Unknown>'
            }

        # Configure Message
        if type(template) is type("") and template.count("{}") is 4:
            self.message = template.format(
                self.context['timestamp'],
                self.context['lineno'],
                self.context['filename'],
                self.context['function']
            )
        elif type(template) is type("") and template.count("{}") is 2:
            self.message = template.format(
                self.context['timestamp'],
                self.context['lineno']
            )
        else:
            self.message = template

        super().__init__(self.message)


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
            message = "[{} {}] " + error_type + ": {}.{}(" + self.url + ")"
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

class InternalServerError(Error):
    """
    Raised when an operation attempts a state transition that's not allowed.

    Attributes:
        message -- explanation of the error
        context -- the meta date of the function which made the server call
    """
    def __init__(self, message=None, context=None):
        super().__init__(message, context)


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

from . import handlers
