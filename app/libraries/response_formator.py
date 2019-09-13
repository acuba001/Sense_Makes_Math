import re
from app.errors.error_types import BadUrlError, ExternalServerError, InternalServerError

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

class myResponse():
    """Work in Progress"""
    def __init__(self, source = None):
        self.source = source or ""
        self.content = {
            'code': None,
            'data': None,
            'error': {
                'reason': None,
                'message': None
            },
            'paging': {
                'total': 0,
                'offset': 0,
                'limit': 0
            }
        }

    def config(self, response):
        isValid = type(response) is type({})
        if isValid:
            self.content['code'] = response['code'] or None
            self.content['data'] = response['results'] or []
            self.content['error']['reason'] = response['error']['reason'] or 'Server Error'
            self.content['error']['message'] = response['error']['message'] or ''
            self.content['paging']['total'] = response['paging']['total'] or 0
            self.content['paging']['offset'] = response['paging']['offset'] or 0
            self.content['paging']['limit'] = response['paging']['limit'] or 0


# def formatErrorMessage(error, context):
#     """Current Version"""
#     err_message = None
#     if context:
#         ln = str(context.lineno or None)
#         fn = str(context.filename.rpartition("/")[2].rpartition(".")[0] or None)
#         fnc = str(context.function or None)
#         template = "[{} , LN {}] An error occured while executing {}::{}. "
#         err_message = template.format(ln, fn, fnc, error)
#     else:
#         template = "Sorry, something went wrong! Please trya gain later. Error Thrown: {}"
#         err_message = template.format(error)
    
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
#         print(res_paging)
#     res_object = {
#         'code': res_code,
#         'data': res_data,
#         'error': res_error,
#         'paging': res_paging
#     }
#     print(res_object)
#     return res_object
