from app import app, cache

import requests

timeout = 60*app.config['YOUTUBE_DATA_FETCH_PER_DAY']/24

def getAllYouTubePlaylists():
    playlist_url = 'https://www.googleapis.com/youtube/v3/playlists'
    playlist_params = {
        'key': app.config['GOOGLE_API_KEY'],
        'part': 'id, player, snippet',
        'channelId': app.config['YOUTUBE_CHANNEL_ID'],
        'maxResults': app.config['YOUTUBE_DATA_MAXRESULTS']
    }
    playlistIds = []
    try:
        # To see what the response object looks like, 
        # please visit : https://developers.google.com/youtube/v3/docs/playlists#resource
        playlist_res = requests.get(playlist_url, params=playlist_params).json() or {}
        playlist_list = playlist_res['items']
    except Exception as err:
        print(err)
    for item in playlist_list:
        if item['kind'] == 'youtube#playlist':
            playlistIds.append({
                'id': item['id'],
                'player': item['player'],
                'snippet': item['snippet'],
            })
    return playlistIds

def getYouTubeVideoIdsByPlaylist(playlistId):
    playlistItems_request_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
    playlistItems_params = {
        'key': app.config['GOOGLE_API_KEY'],
        'part': 'snippet',
        'playlistId': playlistId,
        'maxResults': app.config['YOUTUBE_DATA_MAXRESULTS']
    }
    videoIds = []
    try:
        # To see what the response object looks like, 
        # please visit : https://developers.google.com/youtube/v3/docs/playlistItems
        playlistItems_res = requests.get(playlistItems_request_url, params=playlistItems_params).json() or {}
        playlistItems_list = playlistItems_res['items']
    except Exception as err:
        print(err)
    for item in playlistItems_list:
        videoIds.append(item['snippet']['resourceId']['videoId'])
    return videoIds

def getVideoResourceById(videoId):
    video_request_url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'key': app.config['GOOGLE_API_KEY'],
        'part': 'id, player',
        'id': videoId,
        'maxResults': app.config['YOUTUBE_DATA_MAXRESULTS']
    }
    # To see what the response object looks like, 
    # please visit : https://developers.google.com/youtube/v3/docs/videos#resource
    res = requests.get(video_request_url, params=params)
    return res.json()['items']


@cache.cached(timeout=timeout, key_prefix='getAllYouTubeVideos')
def getAllYouTubeVideos():
    allYouTubeVideos = []
    listOfPLaylistIds = getAllYouTubePlaylists()
    for pl in listOfPLaylistIds:
        listOfVideoIdsByPlaylistId = getYouTubeVideoIdsByPlaylist(pl['id'])
        for vid in listOfVideoIdsByPlaylistId:
            videoResource = getVideoResourceById(vid)[0]
            if videoResource not in allYouTubeVideos:
                videoResource['playlistId'] = pl['id']
                allYouTubeVideos.append(videoResource)
                
    return allYouTubeVideos