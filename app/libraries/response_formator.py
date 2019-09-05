import re
import logging
        
def strip_html(raw_html):
    re.purge()

    # Strip HTML Tags
    template1 = re.compile(r"<.*?>")
    _html = re.sub(template1, '', raw_html)

    # Strip HTML extra characters
    template2 = re.compile(r"/&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});/ig") 
    clean_html = re.sub(template2, '', clean_html)

    clean_html = clean_html.replace('\n', ' ')

    clean_html = clean_html.replace('&nbsp;', '')

    return clean_html

# class myResponse():
"""Work in Progress"""
#     def __init__(self, context = None):
#         self.response = {
#             'code': None,
#             'data': None,
#             'error': {
#                 'reason': None,
#                 'message': None
#             }
#         }
#         self.paging = {
#             'total': 0,
#             'offset': 0,
#             'limit': 0
#         }
#         if not context is None:
#             self.context = {
#                 'timestamp': context['timestamp'] or None,
#                 'lineno': context['lineno'] or None,
#                 'filename': context['filename'] or None,
#                 'function': context['function'] or None
#             }

#     def configureContext(self, context):
#         if not context is None:
#             self.context['timestamp'] = context.timestamp or None
#             self.context['lineno'] = context.lineno or None
#             self.context['filename'] = context.filename.rpartition("/")[2].rpartition(".")[0] or None
#             self.context['function'] = context.function or None

#     def parseErrorMessage(self, error, err_type='api'):
#         err_message = None
#         template1 = "Sorry, something went wrong! Please try gain later. Error Thrown: {}"
#         template2 = "[{} {}] An error occured after calling {}.{}. Error thrown: {}"
#         if err_type is 'api':
#             err_message = template1.format(error)
#         elif err_type is 'local':
#             err_message = template2.format(
#                 context['timestamp'], 
#                 context['lineno'], 
#                 context['filename'], 
#                 context['function'],
#                 error
#                 )
#         self.response['error'] = err_message


#     def configureResponse(self, response, source = 'printful'):
#         if source is 'printful':
#             res_code = response["code"]
#             if res_code in [200]:
#                 res_data = response['result']
#                 res_error = None
#                 res_paging = response['paging'] or None
#             else:
#                 res_data = None
#                 res_error = self.configureErrorMessage(response['error'])
#                 res_paging = None
#         elif source is 'youtube':
#             res_code = response["code"]
#             if res_code in [200]:
#                 res_data = response['items']
#                 res_error = None
#                 res_paging = response['paging'] or None
#             else:
#                 res_data = None
#                 res_error = self.configureErrorMessage(response['error'])
#                 res_paging = None
#         elif source is 'paypal':
#             res_code = response["code"]
#             if res_code in [200]:
#                 res_data = response['result']
#                 res_error = None
#                 res_paging = response['paging'] or None
#             else:
#                 res_data = None
#                 res_error = self.configureErrorMessage(response['error'])
#                 res_paging = None

#         res_object = {
#             'code': res_code,
#             'data': res_data,
#             'error': res_error,
#             'paging': res_paging
#         }
#         print(res_object)
#         self.response = res_object

# def formatErrorMessage(error, context):
"""First Version"""
#     err_message = None
#     template = "[LN {}] An error occured while executing {}.{}. Error thrown: {}" if context != None else "Sorry, something went wrong! Please trya gain later. Error Thrown: {}"
#     if context:
#         ln = str(context.lineno or None)
#         fn = str(context.filename.rpartition("/")[2].rpartition(".")[0] or None)
#         fnc = str(context.function or None)
#         err_message = template.format(ln, fn, fnc, error)
#         template.format(error)

#     return err_message if error != None else str(error)


# def formatResponse(response, context):
#     res_code = response["code"]
#     if res_code != 200:
#         res_data = []
#         res_error = formatErrorMessage(response['result'], context)
#         res_paging = str(None)
#     else:
#         res_data =response["result"]
#         # print(res_data[0])
#         res_error = str(None)
#         res_paging = response["paging"] if response["paging"] else str(None)


def formatErrorMessage(error, context):
    """Current Version"""
    err_message = None
    ln = str(context.lineno or None)
    fn = str(context.filename.rpartition("/")[2].rpartition(".")[0] or None)
    fnc = str(context.function or None)
    template = "[LN {}] An error occured while executing {}.{}. Error thrown: {}" if context else "Sorry, something went wrong! Please trya gain later. Error Thrown: {}"
    err_message = template.format(ln, fn, fnc, error) if context else template.format(error)

    return err_message if error != None else str(error)


def formatResponse(response, context):
    code = response["code"]
    data = [] if not code in [200] else response["result"]
    error = formatErrorMessage(response['result'], context) if not code in [200] else str(None)
    return {
        'code': code,
        'data': data,
        'error': error
    }
