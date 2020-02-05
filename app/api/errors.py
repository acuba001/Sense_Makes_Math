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
            print("Is Context Not None: {}".format('Yes' if isNotNone else 'No'))

            isGoodType = isinstance(context, object)
            print("Is the Context a Good Type: {}".format('Yes' if isGoodType else 'No'))

            isNotEmpty = context is not {}
            print("Is the Context Not Empty: {}".format('Yes' if isNotEmpty else 'No'))

            isValidFields = set(("lineno", "filename", "function")) <= set(dir(context))
            print("Does the Context have valid Fields?: {}".format('Yes' if isValidFields else 'No'))

            return isNotNone and isGoodType and isNotEmpty  # and isValidFields

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
        if isinstance(template, str) and template.count("{}") == 4:
            self.message = template.format(
                self.context['timestamp'],
                self.context['lineno'],
                self.context['filename'],
                self.context['function']
            )
        elif isinstance(template, str) and template.count("{}") == 2:
            self.message = template.format(
                self.context['timestamp'],
                self.context['lineno']
            )
        else:
            self.message = template

        super().__init__(self.message)


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
            message = "[{} {}] " + self.__class__ + ": {}(" + url + ") -- LN {}"
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
            message = "[{} {}]  Error thrown of type: " + error_type + " while callling " + self.url + " [in {}.{}]"
        super().__init__(message, context)
