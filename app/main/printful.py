from app import app, cache

import requests
import inspect

timeout = 60*app.config['PRINTFUL_DATA_FETCH_PER_DAY']/24


# Please See: https://www.printful.com/docs/
 
def handleError(error, context):
    if context:
        err_message = "[LN {}] An error occured while executing {}.{}." 
        + "Error thrown: {}".format(context.lineno, context.filename, context.function, error)
        return {
            'code': 404, 
            'data': [], 
            'error': {
                'reason': None, 
                'message': err_message 
                }
            }

@cache.cached(timeout=timeout, key_prefix='getAllPrintfulData')
def getAllPrintfulData(dataType):
    dataType = dataType if dataType != None else "products"
    ers = []
    video_request_url = 'https://api.printful.com/{}'.format(dataType)
    params = {
        'Authorization': app.config['PRINTFUL_API_KEY']#,
        # 'maxResults': app.config['PRINTFUL_DATA_MAXRESULTS']
    }
    try:
        res = requests.get(video_request_url, params=params).json()
        return {
            'code': res['code'], 
            'data': res['result'], 
            'error': { 
                'reason': res['error']['reason'] or None, 
                'message': res['error']['message'] or None 
                }
            }
    except Exception as err:
        return handleError(err, inspect.stack()[0])