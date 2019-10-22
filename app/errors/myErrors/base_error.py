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
    def __init__(self, template, context):
        def isValidContext(context):
            isNotNone = not context is None
            isGoodType = type(context) is type({})
            isNotEmpty = not context is {}
            isValidLineNo = "lineno" in dir(context)
            isValidFilename = "filename" in dir(context)
            isValidFunction = "function" in dir(context)
            return  isNotNone and isGoodType and isNotEmpty and isValidLineNo and isValidFilename and isValidFunction

        if isValidContext(context):
            cntxt = {
                'timestamp': datetime.now(),
                'lineno': context.lineno or -1,
                'filename': context.filename.rpartition("/")[2].rpartition(".")[0] or "Unknown",
                'function': context.function or "some unknown function"
            }
        else:
            cntxt = {
                'timestamp': datetime.now(),
                'lineno': -1,
                'filename': self.__context__,
                'function': self.__traceback__
            }

        self.context = cntxt

        if type(template) is type("") and template.count("{}") is 4:
            message = template.format(
                self.context['timestamp'],
                self.context['filename'],
                self.context['function'],
                self.context['lineno']
            )
        elif type(template) is type(""):
            message = template

        super(Exception, self).__init__(message)


# from datetime import datetime
# class Error(Exception):
#     """
#     Base class for exceptions in this module.

#     Attributes:
#         context -- the meta data of the function which made the server call
#     """
#     def __init__(self, template = None, context = None):
#         self.message = self.setMessage(template)        
#         self.context = self.setContext(context)

#     def setContext(self, context = None):
#         """
#         Sets the context of the function which threw the 'error'

#         Attributes:
#             context -- the meta data of the function which made the server call
#         """
#         if not context is None:
#             self.context['timestamp'] = str(datetime.now or None)
#             self.context['lineno'] = str(context.lineno or None)
#             self.context['filename'] =str(context.filename.rpartition("/")[2].rpartition(".")[0] or None)
#             self.context['function'] = str(context.function or None)
#         return self

#     def setMessage(self, template = None):
#         """
#         Sets the message of the function which threw the 'error' to 

#         Attributes:
#             template -- the template of the message to be set. 
#         """
#         err_message = None

#         def isValidTemplate(template):
#             return template.count("{}") is 4 or template is None
            
#         if isValidTemplate(template):
#             if template is None: 
#                 template = "[{} , LN {}] An error occured while executing {}::{}. "

#             err_message = template.format(
#                 self.context['timestamp'], 
#                 self.context['lineno'], 
#                 self.context['filename'], 
#                 self.context['function']
#                 )
#         else:
#             raise Exception
        
#         self.message = err_message
#         return self

