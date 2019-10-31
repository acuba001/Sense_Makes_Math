import requests
import inspect
import json

from app import app, cache
from app.errors import *
from app.libraries import myResponse as myRes

timeout = 60*app.config['YOUTUBE_DATA_FETCH_PER_DAY']/24

from abc import ABC, abstractmethod
class XApiController(ABC):

    @property
    @abstractmethod
    def base_url(self):
        pass

#     @base_url.setter
#     @abstractmethod
#     def base_url(self, newUrl):
#         pass

    @abstractmethod
    def get(self, endpoint):
        pass
    
    # @abstractmethod
    # def post(self, endpoint):
    #     pass
    
    # @abstractmethod
    # def put(self, endpoint):
    #     pass
    
    # @abstractmethod
    # def delete(self, endpoint):
    #     pass

class YouTube(XApiController):
    """
    """
    _base_url = "https://www.googleapis.com/youtube/v3/"

    @property
    def base_url(self):
        return self._base_url

    # @base_url.setter
    # def base_url(self, newUrl):
    #     if type(newUrl) is type(""):
    #         self._base_url = newUrl

    @staticmethod
    def isValidPart(part):
        valid_youtube_part =[
            'id',
            'player',
            'snippet'
        ]
        return part in valid_youtube_part
    
    @staticmethod
    def isValidResourceName(endpoint):
        valid_youtube_resources = [
            'activities',
            'channels',
            'channelBanners',
            'channelSections',
            'guideCategories',
            'i18nLanguages',
            'i18nRegions',
            'playlists',
            'playlistItems',
            'search results',
            'subscriptions',
            'thumbnails',
            'videos',
            'videoCategories',
            'watermarks'
        ]
        return endpoint in valid_youtube_resources
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
           
    def get(self, resource_name, endpoint, opts):
        """
        This method will retrive a YouTube Resource
        
        @params: 
            "resource_name" <String> -- A valid YouTube Resource name string
                 "endpoint" <String> -- A valid YouTube Resource endpoint string
                     "opts" <Object> -- An Object containing both required and optional 
                            parameters
        
            For Example, if 

                    "resource_name" = "playlist" and
                    "endpoint" = ''
                    opts.parts =['id', 'snippet'],
        
            then a successfull call to

                    "https://www.googleapis.com/youtube/v3/<resource_name>/<endpoint>"

            would return something like:

                "response":   {
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

                where every "item" in "response.items" will be of the form:

                    "resource":   {
                        "kind": "youtube#playlist",
                        "etag": "etag",
                        "id": "string",
                        "snippet": {
                            "publishedAt": "datetime",
                            "channelId": "string",
                            "title": "string",
                            "description": "string",
                            "thumbnails": {
                            ("key"): {
                                "url": "string",
                                "width": "unsigned integer",
                                "height": "unsigned integer"
                            }
                            },
                            "channelTitle": "string",
                            "tags": [
                            "string"
                            ],
                            "defaultLanguage": "string",
                            "localized": {
                            "title": "string",
                            "description": "string"
                            }
                        },
                        "status": {
                            "privacyStatus": "string"
                        },
                        "contentDetails": {
                            "itemCount": "unsigned integer"
                        },
                        "player": {
                            "embedHtml": "string"
                        },
                        "localizations": {
                            ("key"): {
                            "title": "string",
                            "description": "string"
                            }
                        }
                    }.
        
            An unsuccessful call would return somthing like:

                "response" :  {
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
        # Build the URL string
        # 
        # step 1: Basic Resource Url
        if self.isValidResourceName(resource_name):
            url = self.base_url+resource_name        
        else:
            raise Error(None, inspect.stack()[0])
        #
        # step 2: Load The Endpoint
        if endpoint:
            url += endpoint
        
        # Configure the request parameters
        #
        # Step 1: Load Hidden Values
        params = {
            'key': app.config['GOOGLE_API_KEY'],
            'channelId': app.config['YOUTUBE_CHANNEL_ID'],
            'maxResults': app.config['YOUTUBE_DATA_MAXRESULTS'],
            'part': 'id'
        }
        #
        # Step 2: Load Possible Optional Parameters
        for field in opts.keys():
            if field is 'parts':
                for part in opts["parts"]:
                    if self.isValidPart(part):
                        if part == 'id':
                            continue
                        params['part'] += ", "+part
            elif field is 'pageToken':
                params['pageToken'] = opts["pageToken"]
            elif field is 'publishedAfter':
                params['publishedAfter'] = opts["publishedAfter"]
            elif field is 'publishedBefore':
                params['publishedBefore'] = opts["publishedBefore"]
            elif field is 'regionCode':
                params['regionCode'] = opts["regionCode"]
            elif field is 'playlistId':
                params['playlistId'] = opts["playlistId"]
            elif field is 'videoId':
                params['videoId'] = opts["videoId"]
            elif field is 'id':
                params['id'] = opts["id"]

        # Make a call to the YouTubeData Api.V3 
        try:
            xRes = requests.get(url, params=params)
            # To see what the response object looks like, 
            # please visit : https://developers.google.com/youtube/v3/docs/playlists#resource or 
            # in general: "https://developers.google.com/youtube/v3/docs/< valid#resource >"
            if xRes.ok:
                return xRes.json()
            else:
                raise BadApiCallError("[{} LN {}] YouTubeError("+str(xRes.status_code)+"): " + xRes.message, inspect.stack()[0], 'YouTube', url)
        except Exception as err:
            if type(err) is type(BadApiCallError):
                raise
            else:
                raise Error("[{} {}] InternalServerError: "+str(err), inspect.stack()[0]) 

@cache.cached(timeout=timeout, key_prefix='getAllYouTubeVideos')
def getAllYouTubeVideos():
    """
    
    """
    playlistResources = []
    allYouTubeVideoResources = []
    allYouTubePlaylistItems = []
    try:
        # Grab all 'YouTube' playlistResources
        Options = {'parts':['id']}#, 'player', 'snippet'
        playlist_res = YouTube().get('playlists','/', opts=Options) or {}
        # To see what the response object looks like, 
        # please visit : https://developers.google.com/youtube/v3/docs/playlists#resource
        for item in playlist_res['items']:
            if item['kind'] == 'youtube#playlist':
                playlistResources.append(item)


        # Grab all 'Youtube' playlistItemResources
        for playlistResource in playlistResources:
            Options = {'parts':["snippet"], 'playlistId': playlistResource["id"]}
            playlistItems_res = YouTube().get("playlistItems", "/", opts=Options)
            # To see what the response object looks like, 
            # please visit : https://developers.google.com/youtube/v3/docs/playlistItems
            for item in playlistItems_res['items']:
                if item['snippet']['resourceId']['kind'] == 'youtube#video':
                    item['playlistResource'] = playlistResource
                    allYouTubePlaylistItems.append(item)


        # Sort the list of 'playlistItemResources', chronologically, by the 'publishedAt' date     
        allYouTubePlaylistItems_sorted = sorted(allYouTubePlaylistItems, key=lambda x: x["snippet"]["publishedAt"])


        # Grab all 'YouTube' videoResources by 'videoId'
        for playlistItem in allYouTubePlaylistItems_sorted:
            Options = {'parts':["id"], 'id': playlistItem["snippet"]["resourceId"]["videoId"]}
            resource = YouTube().get("videos", "/", opts=Options)['items'][0]
            # To see what the response object looks like, 
            # please visit : https://developers.google.com/youtube/v3/docs/videos#resource
            resource["playlistResource"] = playlistItem["playlistResource"]            
            if resource not in allYouTubeVideoResources:
                allYouTubeVideoResources.append(resource)

    except Exception:
            raise

    return allYouTubeVideoResources

@cache.cached(timeout=timeout, key_prefix='getLatestYouTubeVideo')
def getLatestYouTubeVideo():
    list_of_video_resources = getAllYouTubeVideos()
    return list_of_video_resources.pop()

@cache.cached(timeout=timeout, key_prefix='getYouTubeVideosByPlaylist')
def getYouTubeVideosByPlaylist():
    allVideosByPlaylistBuckets = []
    Options = {'parts':["id"]}
    playlistResources = YouTube().get("playlists", "/", opts=Options)
    # Grab all 'Youtube' playlistItemResources
    for playlistResource in playlistResources:
        Options = {'parts':["snippet"], 'playlistId': playlistResource["id"] }
        playlistItems_res = YouTube().get("playlistItems", "/", opts=Options)
        # To see what the response object looks like, 
        # please visit : https://developers.google.com/youtube/v3/docs/playlistItems
        playlistResource["playlistItems"] = playlistItems_res['items']
        allVideosByPlaylistBuckets.push(playlistResource)
    
    return allVideosByPlaylistBuckets

