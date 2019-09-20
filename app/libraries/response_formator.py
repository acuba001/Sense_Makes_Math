import re
from app.errors.error_types import BadUrlError, ExternalServerError, InternalServerError

def strip_html(raw_html):
    re.purge()

    # Strip HTML Tags
    template1 = re.compile(r"<.*?>")
    _html = re.sub(template1, '', raw_html)

    # Strip HTML extra characters
    template2 = re.compile(r"/&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});/ig") 
    clean_html = re.sub(template2, '', _html)

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
        if type(response) is type({}):
            self.content['error']['reason'] = 'Internal Server Error'
            self.content['error']['message'] = 'Fatal Server Error: Something...went wrong'

            self.content['code'] = response['code']
            self.content['data'] = response['results']

            if type(response['error']) is type({}):
                if 'reason' in response['error'].keys():
                    self.content['error']['reason'] = response['error']['reason']
                
                if 'message' in response['error'].keys():
                    self.content['error']['message'] = response['error']['message']

            if type(response['error']) is type(''):
                self.content['error']['message'] = response['error']
            
            if type(response['error']) is type(None):
                self.content['error']['reason'] = None
                self.content['error']['message'] = None

            if 'paging' in response.keys() and type(response['paging']) is type({}):
                if 'total' in response['paging'].keys():
                    self.content['paging']['total'] = response['paging']['total']

                if 'offset' in response['paging'].keys():
                    self.content['paging']['offset'] = response['paging']['offset']

                if 'limit' in response['paging'].keys():
                    self.content['paging']['limit'] = response['paging']['limit']

        return self.content
