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
    def __init__(self, source = None, res = None):
        self.source = source or ""
        self.xRes = res
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
        isValid = type(response) is type({}) or response["error"] is None
        isString = type(response["error"]) is type("")
        if isValid:
            self.content['code'] = response['code'] or 404
            self.content['data'] = response['results'] or []
            if response['error']['reason']:
                self.content['error']['reason'] = response['error']['reason']
            elif response['error']['message']:
                self.content['error']['message'] = response['error']['message']
            elif isString:
                self.content['error']['message'] = response['error']
            else:
                self.content['error'] = None
        return self.content
           

# def formatErrorMessage(error, context):
#     """Current Version"""
#     err_message = None
#     ln = str(context.lineno or None)
#     fn = str(context.filename.rpartition("/")[2].rpartition(".")[0] or None)
#     fnc = str(context.function or None)
#     template = "[LN {}] An error occured while executing {}.{}. Error thrown: {}" if context else "Sorry, something went wrong! Please trya gain later. Error Thrown: {}"
#     err_message = template.format(ln, fn, fnc, error) if context else template.format(error)

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
