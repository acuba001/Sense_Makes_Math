from app import app, cache

import requests
import inspect

timeout = 60*app.config['PRINTFUL_DATA_FETCH_PER_DAY']/24

# Please See: https://www.printful.com/docs/
 
def handleError(name, error):
    print("An error occured while executing @{}. Error thrown: {}".format(name, error))

def getFromPrintful(type, someId):
    video_request_url = 'https://api.printful.com/'
    params = {
        'Authorization': app.config['PRINTFUL_API_KEY'],
        'maxResults': app.config['YOUTUBE_DATA_MAXRESULTS']
    }
    try:
        res = requests.get(video_request_url, params=params)
        return res.json()['items']
    except Exception as err:
        handleError(inspect.stack()[0][3], err)