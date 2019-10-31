from .base_error import Error # extends the 'Exception' class

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
