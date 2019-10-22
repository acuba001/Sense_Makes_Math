from flask_restful import Resource
import requests
import inspect

from app import app, cache
from app.errors import BadApiCallError, BadUrlError, ArithmeticOperationError, TypeMatchError, Error
from app.libraries import myResponse

timeout = 60*app.config['YOUTUBE_DATA_FETCH_PER_DAY']/24
 
class YouTubeController(Resource):
    """
    """
    def __init__(self):
        self.base_url = "https://www.googleapis.com/youtube/v3/{}"
    
    def isValidEndpoint(self, endpoint):
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

    def isValidPart(self, part):
        return True

    def isValidChannelId(self, channelId):
        return True
            
    def get(self, endpoint, opts = {}):
        context = inspect.stack()[0]
       
        # [WIP] This current only works with base endpoints. 
        # We need to expand the 'isValid' function to deal with
        # other cases
        # 
        if self.isValidEndpoint(self=self, endpoint=endpoint):
            url = self.base_url.format(str(endpoint))
        else:
            raise BadUrlError(None, context)

        # url = self.base_url.format(str(endpoint))w

        params = {
            'key': app.config['GOOGLE_API_KEY'],
            'part': 'id',
            'channelId': app.config['YOUTUBE_CHANNEL_ID'],
            'maxResults': app.config['YOUTUBE_DATA_MAXRESULTS']
        }
        for field in opts.keys():
            if field is 'part':
                part = opts['part']
                if self.isValidPart(part):
                    params['part'] = part
            elif field is 'channelId':
                channelId = opts['channelId']
                if self.isValidChannelId(channelId):
                    params['channelId'] = channelId
        

        # To see what the response object looks like, 
        # please visit : https://developers.google.com/youtube/v3/docs/playlists#resource
        xRes = requests.get(url, params=params).json()
        print(xRes)

        # if xRes["code"] in [200]:
        #     # Return formated response
        #     return  xRes['items']
        # else:
        #     raise ExternalServerError("youtube", url, None, context)

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
