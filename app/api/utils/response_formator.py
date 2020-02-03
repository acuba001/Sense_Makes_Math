import re
# from app.errors import BadApiCallError, Error


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
    def __init__(self, source=None, res=None):
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
        if isinstance(response, {}):
            self.content['code'] = response['code']
            self.content['data'] = response['results']

            if isinstance(response['error'], None):
                self.content['error']['reason'] = None
                self.content['error']['message'] = None

            elif isinstance(response['error'], ""):
                self.content['error']['message'] = response['error']

            elif isinstance(response['error'], {}):
                if 'reason' in response['error'].keys():
                    self.content['error']['reason'] = response['error']['reason']

                if 'message' in response['error'].keys():
                    self.content['error']['message'] = response['error']['message']

        return self.content
