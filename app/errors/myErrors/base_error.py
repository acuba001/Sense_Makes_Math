from datetime import datetime

class Error(Exception):
    """
    Base class for exceptions in this project.

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

    """
    def __init__(self, template, context=None):
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


