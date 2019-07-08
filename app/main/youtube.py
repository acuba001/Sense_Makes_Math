# TodoList
# 1) [TODO] Scrape the names of all the methods accepted as 
# parameters from the site: https://developers.google.com/youtube/v3/docs/
#
# 2) [TODO] Create a pidgeon-box for all playlists associated with 'channelId'.
# the keys  will be the 'playlistId' and the values will be the list of all videos
# associated with both 'channelId' and 'playlistId'
#
# 3) [TODO] Incorporate the the 'pidgeon-box' into the router
#
#
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

    # [NOTE] DO NOT DELETE UNTIL IT IS INCORPORATED INTO THE ROUTER 
    #                                         
    # This is the schema of each item in the list returned by
    # making a 'GET' request to 'https://www.googleapis.com/youtube/v3/search'
    #
    # {
    #   "kind": "youtube#searchResult",
    #   "etag": etag,
    #   "id": {
    #     "kind": string,
    #     "videoId": string,
    #     "channelId": string,
    #     "playlistId": string
    #   },
    #   "snippet": {
    #     "publishedAt": datetime,
    #     "channelId": string,
    #     "title": string,
    #     "description": string,
    #     "thumbnails": {
    #       (key): {
    #         "url": string,
    #         "width": unsigned integer,
    #         "height": unsigned integer
    #       }
    #     },
    #     "channelTitle": string,
    #     "liveBroadcastContent": string
    #   }
    # }  
    res = requests.get(url, params=params)
    return res.json()['items']

def getAllYouTubePlaylists():
    url = 'https://www.googleapis.com/youtube/v3/playlists'
    params = {
        'key': app.config['GOOGLE_API_KEY'],
        'channelId': app.config['YOUTUBE_CHANNEL_ID'],
        'part': 'id',
        'order': 'date',
        'maxResults': app.config['YOUTUBE_DATA_MAXRESULTS']
    }

    # [NOTE] DO NOT DELETE UNTIL IT IS INCORPORATED INTO THE ROUTER  
    #                                         
    # This is the schema of each item in the list returned by
    # making a 'GET' request to 'https://www.googleapis.com/youtube/v3/playlists'
    # 
    # {
    #   "kind": "youtube#playlist",                                                 
    #   "etag": etag,
    #   "id": string,
    #   "snippet": {
    #     "publishedAt": datetime,
    #     "channelId": string,
    #     "title": string,
    #     "description": string,
    #     "thumbnails": {
    #       (key): {
    #         "url": string,
    #         "width": unsigned integer,
    #         "height": unsigned integer
    #       }
    #     },
    #     "channelTitle": string,
    #     "tags": [
    #       string
    #     ],
    #     "defaultLanguage": string,
    #     "localized": {
    #       "title": string,
    #       "description": string
    #     }
    #   },
    #   "status": {
    #     "privacyStatus": string
    #   },
    #   "contentDetails": {
    #     "itemCount": unsigned integer
    #   },
    #   "player": {
    #     "embedHtml": string
    #   },
    #   "localizations": {
    #     (key): {
    #       "title": string,
    #       "description": string
    #     }
    #   }
    # }
    #
    res = requests.get(url, params=params)
    return res.json()['items']
