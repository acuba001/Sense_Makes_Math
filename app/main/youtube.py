from app import app, cache

import requests
import inspect

timeout = 60*app.config['YOUTUBE_DATA_FETCH_PER_DAY']/24
 
def handleError(name, error):
    print("An error occured while executing @{}. Error thrown: {}".format(name, error))

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
    except Exception as err:
        handleError(inspect.stack()[0][3], err)

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
    except Exception as err:
        handleError(inspect.stack()[0][3], err)

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
    except Exception as err:
        handleError(inspect.stack()[0][3], err)


@cache.cached(timeout=timeout, key_prefix='getAllYouTubeVideos')
def getAllYouTubeVideos():
    allYouTubeVideoUnits = []
    allYouTubePlaylistItems = []
    try:
        listOfPLaylistResources = getAllYouTubePlaylistResources()
        # Grab all 'Youtube' videoUnits
        for playlistResource in listOfPLaylistResources:
            listOfPlaylistItems = getYouTubeVideoPlaylistItems(playlistResource['id'])
            for item in listOfPlaylistItems:
                item['playlistResource'] = playlistResource
                allYouTubePlaylistItems.append(item)
        
        # Sort the list chronologically by 'publishedDate'        
        allYouTubePlaylistItems_sorted = sorted(allYouTubePlaylistItems, key=lambda x: x["snippet"]["publishedAt"])

        # Grab all 'YouTube' videos by 'videoId'
        for playlistItem in allYouTubePlaylistItems_sorted:
            videoResource = getYouTubeVideoResource(playlistItem["snippet"]["resourceId"]["videoId"])[0]
            videoUnit = {
                'videoResource': videoResource, 
                'playlistResource': playlistItem['playlistResource']
                }
            if videoUnit not in allYouTubeVideoUnits:
                allYouTubeVideoUnits.append(videoUnit)
        # print(allYouTubeVideoUnits[0] or "It was empty, you fucked up")
        return allYouTubeVideoUnits
    except Exception as err:
        handleError(inspect.stack()[0][3], err)
