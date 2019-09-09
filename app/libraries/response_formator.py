import re

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
    def __init__(self, context = None):
        self.response = {
            'code': None,
            'data': None,
            'error': {
                'reason': None,
                'message': None
            }
        }
        self.paging = {
            'total': 0,
            'offset': 0,
            'limit': 0
        }

    def config(self, response, source = 'printful'):
        res_code = response["code"]
        if source is 'printful':
            if res_code in [200]:
                res_data = response['result']
                res_error = None
                res_paging = response['paging'] or None
            else:
                res_data = None
                res_error = self.configureErrorMessage(response['error'])
                res_paging = None
        elif source is 'youtube':
            if res_code in [200]:
                res_data = response['items']
                res_error = None
                res_paging = response['paging'] or None
            else:
                res_data = None
                res_error = self.configureErrorMessage(response['error'])
                res_paging = None

        res_object = {
            'code': res_code,
            'data': res_data,
            'error': res_error,
            'paging': res_paging
        }
        print(res_object)
        self.response = res_object

def formatErrorMessage(error, context):
    """Current Version"""
    err_message = None
    context = context
    if context:
        ln = str(context.lineno or None)
        fn = str(context.filename.rpartition("/")[2].rpartition(".")[0] or None)
        fnc = str(context.function or None)
        template = "[{} , LN {}] An error occured while executing {}::{}. "
        err_message = template.format(ln, fn, fnc, error)
    else:
        template = "Sorry, something went wrong! Please trya gain later. Error Thrown: {}"
        err_message = template.format(error)
    
    return err_message if error != None else str(error)


def formatResponse(response, context):
    res_code = response["code"]
    if res_code != 200:
        res_data = []
        res_error = formatErrorMessage(response['result'], context)
        res_paging = str(None)
    else:
        res_data =response["result"]
        # print(res_data[0])
        res_error = str(None)
        res_paging = response["paging"] if response["paging"] else str(None)
        print(res_paging)
    res_object = {
        'code': res_code,
        'data': res_data,
        'error': res_error,
        'paging': res_paging
    }
    print(res_object)
    return res_object
