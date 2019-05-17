from app import app, cache

import requests

timeout = 60*app.config['YOUTUBE_DATA_FETCH_PER_DAY']/24

@cache.cached(timeout=timeout, key_prefix='getYouTubeData')
def getYouTubeData():
    
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'key': app.config['GOOGLE_API_KEY'],
        'channelId': app.config['YOUTUBE_CHANNEL_ID'],
        'part': 'id',
        'order': 'date',
        'maxResults': app.config['YOUTUBE_DATA_MAXRESULTS']
    }
    
    res = requests.get(url, params=params)
    return res.json()['items']