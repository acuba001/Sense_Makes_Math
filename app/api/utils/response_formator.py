from flask import Response


class Res(Response):
    """
    """
    _content = {
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

    def __init__(self, source=None, res=None, *args, **kwargs):
        self.source = source
        self.xRes = res
        self.content = self._content
        super(Response, self).__init__(*args, **kwargs)

    def __repr__(self):
        pass

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
