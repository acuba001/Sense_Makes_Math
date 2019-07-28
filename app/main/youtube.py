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

@cache.cached(timeout=timeout, key_prefix='getAllYouTubePlaylists')
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

@cache.cached(timeout=timeout, key_prefix='getAllYouTubeVideosByPlaylistId')
def getAllYouTubeVideosByPlaylistId():
    url = 'https://www.googleapis.com/youtube/v3/playlistItems'
    params = {
        'key': app.config['GOOGLE_API_KEY'],
        'channelId': app.config['YOUTUBE_CHANNEL_ID'],
        'part': 'id',
        'playlistId': 'date',
        'maxResults': app.config['YOUTUBE_DATA_MAXRESULTS'],
        'onBehalfOfContentOwner': '',
        'pageToken': app.config['YOUTUBE_PAGE_TOKEN'],
        'videoId': ""
    }
    # [NOTE] DO NOT DELETE UNTIL IT IS INCORPORATED INTO THE ROUTER  
    #                                         
    # This is the schema of each item in the list returned by
    # making a 'GET' request to 'https://developers.google.com/youtube/v3/docs/playlistItems/list'
    # 
    #     {
    #   "kind": "youtube#playlistItemListResponse",
    #   "etag": etag,
    #   "nextPageToken": string,
    #   "prevPageToken": string,
    #   "pageInfo": {
    #     "totalResults": integer,
    #     "resultsPerPage": integer
    #   },
    #   "items": [
    #     playlistItem Resource
    #   ]
    # }
    res = requests.get(url, params=params)
    return res.json()['items']