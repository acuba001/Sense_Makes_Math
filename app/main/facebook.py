from app import app, cache

import requests

timeout = 60*app.config['FACEBOOK_DATA_FETCH_PER_DAY']/24

@cache.cached(timeout=timeout, key_prefix='getFacebookPosts')
def getFacebookPosts():

    url = 'https://www.graph-video.facebook.com/'
    params = {
        'key': app.config['FACEBOOK_APP_ID'],
        'channelId': app.config['FACEBOOK_APP_ID'],
        'part': 'id',
        'order': 'date',
        'maxResults': app.config['FACEBOOK_DATA_MAXRESULTS']
    }

    res = requests.get(url, params=params)
    return res.json()['items']
