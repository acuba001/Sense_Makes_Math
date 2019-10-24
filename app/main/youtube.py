from flask_restful import Resource
import requests
import inspect

from app import app, cache
from app.errors import BadApiCallError, BadUrlError, InternalServerError, Error
from app.libraries import myResponse as myRes

timeout = 60*app.config['YOUTUBE_DATA_FETCH_PER_DAY']/24


# ====================================================================================
# Basic Operations on YouTube Resources
# 
#   Operation                    Description
# ====================================================================================
# list	        |   Retrieves (GET) a list of zero or more resources.
# ------------------------------------------------------------------------------------
# insert	    |   Creates (POST) a new resource.
# ------------------------------------------------------------------------------------
# update	    |   Modifies (PUT) an existing resource to reflect data in your request.
# ------------------------------------------------------------------------------------
# delete	    |   Removes (DELETE) a specific resource.
# -------------------------------------------------------------------------------------


# =================================================================  
# Supported Operations on YouTube Resources
# 
#   Resource            list        insert      update      delete  
# =================================================================
# activity          |   true    |   true    |   false   |   false			
# caption			|   true    |   true    |   true    |   true   	
# channel           |   true    |   false   |   false   |   false
# channelBanner		|   false   |   true    |   false   |   false 
# channelSection	|   true    |   true    |   true    |   true			
# comment		    |   true    |   true    |   true    |   true
# commentThread		|   true    |   true    |   true    |   false
# guideCategory		|   true    |   false   |   false   |   false   		
# i18nLanguage		|   true    |   false   |   false   |   false   		
# i18nRegion		|   true    |   false   |   false   |   false  		
# playlist			|   true    |   true    |   true    |   true   	
# playlistItem		|   true    |   true    |   true    |   true   		
# search result		|   true    |   false   |   false   |   false  		
# subscription		|   true    |   false   |   false   |   false  		
# thumbnail			|   false   |   false   |   false   |   false 	
# video				|   true    |   true    |   true    |   true
# videoCategory		|   true    |   false   |   false   |   false    		
# watermark			|   false   |   false   |   false   |   false 
# ----------------------------------------------------------------
from abc import ABC, abstractmethod

class XApiController(ABC):

    @property
    @abstractmethod
    def base_url(self):
        pass

    @base_url.setter
    @abstractmethod
    def base_url(self, newUrl):
        pass

    @abstractmethod
    def get(self, endpoint):
        pass
    
    @abstractmethod
    def post(self, endpoint):
        pass
    
    @abstractmethod
    def put(self, endpoint):
        pass
    
    @abstractmethod
    def delete(self, endpoint):
        pass

class YouTube(XApiController):
    """
    """
    _base_url = "https://www.googleapis.com/youtube/v3/{}"

    @property
    def base_url(self):
        return self.base_url

    @base_url.setter
    def base_url(self, newUrl):
        if isValidUrl(newUrl):
            self.base_url = newUrl
        else:
            self.base_url = _base_url
    
    @staticmethod
    def isValidEndpoint(endpoint):
        pass
    
    @staticmethod
    def isValidResourceName(endpoint):
        valid_youtube_resources = [
            'activity',
            'channel',
            'channelBanner',
            'channelSection',
            'guideCategory',
            'i18nLanguage',
            'i18nRegion',
            'playlist',
            'playlistItem',
            'search result',
            'subscription',
            'thumbnail',
            'video',
            'videoCategory',
            'watermark'
        ]
        return endpoint in valid_youtube_resources

    @staticmethod
    def isValidPart(part):
        valid_youtube_part =[
            'id',
            'player',
            'snippet'
        ]
        return part in valid_youtube_part

    @staticmethod   
    def isValidUrl(url):
        return True
            
    def get(self, resource_name, endpoint, opts):
        """
        This method will make a, GET, call to 

        and will return JSON onject containing a list of resources. 
        
        
        params:
            resource_name -- A valid YouTube Resource name string
                 endpoint -- A valid YouTube Resource endpoint string
                    opts -- An Object containing both required and optional 
                            parameters
        
        For Example, if 

                resource_name = playlist and
                endpoint = ''
                opts.parts =['id', 'snippet'],
        
        then a successfull call to

                "https://www.googleapis.com/youtube/v3/<resource_name>/<endpoint>"

        would return something like:
                {
                    "kind": "youtube#activityListResponse",
                    "etag": etag,
                    "nextPageToken": string,
                    "prevPageToken": string,
                    "pageInfo": {
                        "totalResults": integer,
                        "resultsPerPage": integer
                    },
                    "items": [
                        activity Resource
                    ]
                },

        where all items will be of the form:

                {
                    "kind": "youtube#playlist",
                    "etag": etag,
                    "id": string,
                    "snippet": {
                        "publishedAt": datetime,
                        "channelId": string,
                        "title": string,
                        "description": string,
                        "thumbnails": {
                        (key): {
                            "url": string,
                            "width": unsigned integer,
                            "height": unsigned integer
                        }
                        },
                        "channelTitle": string,
                        "tags": [
                        string
                        ],
                        "defaultLanguage": string,
                        "localized": {
                        "title": string,
                        "description": string
                        }
                    },
                    "status": {
                        "privacyStatus": string
                    },
                    "contentDetails": {
                        "itemCount": unsigned integer
                    },
                    "player": {
                        "embedHtml": string
                    },
                    "localizations": {
                        (key): {
                        "title": string,
                        "description": string
                        }
                    }
                }.
        
        An unsuccessful call would return somthing like:
                {
                    "error": {
                    "errors": [
                    {
                        "domain": "youtube.parameter",
                        "reason": "missingRequiredParameter",
                        "message": "No filter selected. Expected one of: home, channelId, mine",
                        "locationType": "parameter",
                        "location": ""
                    }
                    ],
                    "code": 400,
                    "message": "No filter selected. Expected one of: home, channelId, mine"
                    }
                } 
                            
        """
        # [WIP] This current only works with base endpoints. 
        # We need to expand the 'isValid' function to deal with
        # other cases
        # 
        if self.isValidResourceName(resource_name):
            url = _base_url.format(str(resource_name))
            if self.isValidEndpoint(endpoint):
                url += endpoint
            else:
                raise BadUrlError(None, inspect.stack()[0])
        else:
            raise BadApiCallError(None, inspect.stack()[0])

        params = {
            'key': app.config['GOOGLE_API_KEY'],
            'channelId': app.config['YOUTUBE_CHANNEL_ID'],
            'maxResults': app.config['YOUTUBE_DATA_MAXRESULTS'],
            'part': 'id'
        }
        for field in opts.keys():
            if field is 'parts':         
                for part in opts.parts:
                    if part == 'id':
                        continue
                    if isValidPart(part):
                        params['part'] += ", "+part
            elif field is 'pageToken':
                params['pageToken'] = opts.pageToken
            elif field is 'publishedAfter':
                params['publishedAfter'] = opts.publishedAfter
            elif field is 'publishedBefore':
                params['publishedBefore'] = opts.publishedBefore
            elif field is 'regionCode':
                params['regionCode'] = opts.regionCode
            

        # To see what the response object looks like, 
        # please visit : https://developers.google.com/youtube/v3/docs/playlists#resource
        xRes = requests.get(url, params=params).json()
        print(xRes)

        # if xRes["code"] in [200]:
        #     # Return formated response
        #     return  xRes['items']
        # else:
        #     raise InternalServerError(None, context, "youtube", url,)

        # playlistResources = []
        # list_of_playlists = xRes['items']
        # for item in list_of_playlists:
        #     if item['kind'] == 'youtube#playlist': 
        #         playlistResources.append(item)
        # return playlistResources

def getAllYouTubePlaylistResources():
    playlist_url = 'https://www.googleapis.com/youtube/v3/playlists'
    playlist_params = {
        'key': app.config['GOOGLE_API_KEY'],
        'part': 'id, player, snippet',
        'channelId': app.config['YOUTUBE_CHANNEL_ID'],
        'maxResults': app.config['YOUTUBE_DATA_MAXRESULTS']
    }
    playlistResources = []
    try:
        # To see what the response object looks like, 
        # please visit : https://developers.google.com/youtube/v3/docs/playlists#resource
        playlist_res = requests.get(playlist_url, params=playlist_params).json() or {}

        playlist_list = playlist_res['items']
        for item in playlist_list:
            isPlaylist =  item['kind'] == 'youtube#playlist'
            if isPlaylist: 
                playlistResources.append(item)

        return playlistResources
    except Exception:
        raise  BadApiCallError(None, inspect.stack()[0])

def getYouTubeVideoPlaylistItems(playlistId):
    playlistItems_request_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
    playlistItems_params = {
        'key': app.config['GOOGLE_API_KEY'],
        'part': 'snippet',
        'playlistId': playlistId,
        'maxResults': app.config['YOUTUBE_DATA_MAXRESULTS']
    }
    playlistItemBucket = []
    try:
        # To see what the response object looks like, 
        # please visit : https://developers.google.com/youtube/v3/docs/playlistItems
        playlistItems_res = requests.get(playlistItems_request_url, params=playlistItems_params).json()
        playlistItems_list = playlistItems_res['items']
        for item in playlistItems_list:
            isVideo = item['snippet']['resourceId']['kind'] == 'youtube#video'
            if isVideo:
                playlistItemBucket.append(item)
        
        return playlistItemBucket
    except Exception:
        raise BadApiCallError(None, inspect.stack()[0])

def getYouTubeVideoResource(videoId):
    video_request_url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'key': app.config['GOOGLE_API_KEY'],
        'part': 'id, player, snippet',
        'id': videoId,
        'maxResults': app.config['YOUTUBE_DATA_MAXRESULTS']
    }
    try:
        # To see what the response object looks like, 
        # please visit : https://developers.google.com/youtube/v3/docs/videos#resource
        res = requests.get(video_request_url, params=params)
        return res.json()['items']
    except Exception:
        raise BadApiCallError(None, inspect.stack()[0])


@cache.cached(timeout=timeout, key_prefix='getAllYouTubeVideos')
def getAllYouTubeVideos():
    allYouTubeVideoResources = []
    allYouTubePlaylistItems = []
    try:
        listOfPLaylistResources = getAllYouTubePlaylistResources()
        # Grab all 'Youtube' videoResources
        for playlistResource in listOfPLaylistResources:
            listOfPlaylistItems = getYouTubeVideoPlaylistItems(playlistResource['id'])
            for item in listOfPlaylistItems:
                item['playlistResource'] = playlistResource
                allYouTubePlaylistItems.append(item)
        
        # Sort the list, chronologically, by the 'publishedAt' date     
        allYouTubePlaylistItems_sorted = sorted(allYouTubePlaylistItems, key=lambda x: x["snippet"]["publishedAt"])

        # Grab all 'YouTube' videos by 'videoId'
        for playlistItem in allYouTubePlaylistItems_sorted:
            resource = getYouTubeVideoResource(playlistItem["snippet"]["resourceId"]["videoId"])[0]
            resource["playlistResource"] = playlistItem['playlistResource']
            if resource not in allYouTubeVideoResources:
                allYouTubeVideoResources.append(resource)
        return allYouTubeVideoResources
    except Exception:
        raise BadApiCallError(None, inspect.stack()[0])
