from app import cache
from flask import current_app
from ..errors import Error
from app.api.utils import sdk


video_timeout = 60 * current_app.config['YOUTUBE_DATA_FETCH_PER_DAY'] / 24
@cache.cached(timeout=video_timeout, key_prefix='getAllVideos')
def getAllVideos():
    """

    """
    playlistResources = []
    allVideoResources = []
    allPlaylistItems = []
    try:
        # Grab all 'YouTube' playlistResources
        Options = {
            'parts': ['id']  # , 'player', 'snippet'
        }
        playlist_res = sdk.YouTube().get('playlists', '/', opts=Options) or {}
        # To see what the response object looks like,
        # please visit : https://developers.google.com/youtube/v3/docs/playlists#resource
        for item in playlist_res['items']:
            if item['kind'] == 'youtube#playlist':
                playlistResources.append(item)

        # Grab all 'Youtube' playlistItemResources
        for playlistResource in playlistResources:
            Options = {
                'parts': ["snippet"],
                'playlistId': playlistResource["id"]
            }
            playlistItems_res = sdk.YouTube().get("playlistItems", "/", opts=Options)
            # To see what the response object looks like,
            # please visit : https://developers.google.com/youtube/v3/docs/playlistItems
            for item in playlistItems_res['items']:
                if item['snippet']['resourceId']['kind'] == 'youtube#video':
                    item['playlistResource'] = playlistResource
                    allPlaylistItems.append(item)

        # Sort the list of 'playlistItemResources', chronologically, by the 'publishedAt' date
        allPlaylistItems_sorted = sorted(
            allPlaylistItems, key=lambda x: x["snippet"]["publishedAt"])

        # Grab all 'YouTube' videoResources by 'videoId'
        for playlistItem in allPlaylistItems_sorted:
            Options = {
                'parts': ["id"],
                'id': playlistItem["snippet"]["resourceId"]["videoId"]
            }
            resource = sdk.YouTube().get("videos", "/", opts=Options)['items'][0]
            # To see what the response object looks like,
            # please visit : https://developers.google.com/youtube/v3/docs/videos#resource
            resource["playlistResource"] = playlistItem["playlistResource"]
            if resource not in allVideoResources:
                allVideoResources.append(resource)

    except Exception as err:
        raise Error(err, None)

    return allVideoResources


@cache.cached(timeout=video_timeout, key_prefix='getLatestVideo')
def getLatestVideo():
    list_of_video_resources = []
    try:
        list_of_video_resources.extend(getAllVideos())
    except Exception:
        raise

    return list_of_video_resources.pop()


@cache.cached(timeout=video_timeout, key_prefix='getVideosByPlaylist')
def getVideosByPlaylist():
    allVideosByPlaylistBuckets = []
    try:
        # Grab all 'Youtube' playlistResources
        Options = {
            'parts': ["id", "snippet"]  #
        }
        playlistResource_res = sdk.YouTube().get("playlists", "/", opts=Options)
        # To see what the response object looks like,
        # please visit : https://developers.google.com/youtube/v3/docs/playlists#resource

        for playlistResource in playlistResource_res["items"]:
            Options = {
                'parts': ["id", "snippet"],
                'playlistId': playlistResource["id"]
            }
            playlistItems_res = sdk.YouTube().get("playlistItems", "/", opts=Options)
            # To see what the response object looks like,
            # please visit : https://developers.google.com/youtube/v3/docs/playlistItems

            playlistVideoIds = [item["snippet"]["resourceId"]["videoId"]
                                for item in playlistItems_res['items']]

            playlistResource["videoResources"] = []
            for id in playlistVideoIds:

                Options = {
                    'parts': ["id"],
                    'id': id
                }
                resource = sdk.YouTube().get("videos", "/", opts=Options)['items'][0]

                playlistResource["videoResources"].append(resource)
                # To see what the response object looks like,
                # please visit : https://developers.google.com/youtube/v3/docs/videos#resource

            allVideosByPlaylistBuckets.append(playlistResource)
    except Exception:
        raise

    return allVideosByPlaylistBuckets


# #
# video_timeout = 60 * current_app.config['YOUTUBE_DATA_FETCH_PER_DAY'] / 24
# @cache.cached(timeout=video_timeout, key_prefix='getAllVideos')
# def getAllVideos():
#     """

#     """
#     playlistResources = []
#     allVideoResources = []
#     allPlaylistItems = []
#     try:
#         # Grab all 'YouTube' playlistResources
#         Options = {
#             'parts': ['id']  # , 'player', 'snippet'
#         }
#         playlist_res = sdk.YouTube().get('playlists', '/', opts=Options) or {}
#         # To see what the response object looks like,
#         # please visit : https://developers.google.com/youtube/v3/docs/playlists#resource
#         for item in playlist_res['items']:
#             if item['kind'] == 'youtube#playlist':
#                 playlistResources.append(item)

#         # Grab all 'Youtube' playlistItemResources
#         for playlistResource in playlistResources:
#             Options = {
#                 'parts': ["snippet"],
#                 'playlistId': playlistResource["id"]
#             }
#             playlistItems_res = sdk.YouTube().get("playlistItems", "/", opts=Options)
#             # To see what the response object looks like,
#             # please visit : https://developers.google.com/youtube/v3/docs/playlistItems
#             for item in playlistItems_res['items']:
#                 if item['snippet']['resourceId']['kind'] == 'youtube#video':
#                     item['playlistResource'] = playlistResource
#                     allPlaylistItems.append(item)

#         # Sort the list of 'playlistItemResources', chronologically, by the 'publishedAt' date
#         allPlaylistItems_sorted = sorted(
#             allPlaylistItems, key=lambda x: x["snippet"]["publishedAt"])

#         # Grab all 'YouTube' videoResources by 'videoId'
#         for playlistItem in allPlaylistItems_sorted:
#             Options = {
#                 'parts': ["id"],
#                 'id': playlistItem["snippet"]["resourceId"]["videoId"]
#             }
#             resource = sdk.YouTube().get("videos", "/", opts=Options)['items'][0]
#             # To see what the response object looks like,
#             # please visit : https://developers.google.com/youtube/v3/docs/videos#resource
#             resource["playlistResource"] = playlistItem["playlistResource"]
#             if resource not in allVideoResources:
#                 allVideoResources.append(resource)

#     except Exception as err:
#         raise Error(err)

#     return allVideoResources


# @cache.cached(timeout=video_timeout, key_prefix='getLatestVideo')
# def getLatestVideo():
#     list_of_video_resources = []
#     try:
#         list_of_video_resources.extend(getAllVideos())
#     except Exception:
#         raise

#     return list_of_video_resources.pop()


# @cache.cached(timeout=video_timeout, key_prefix='getVideosByPlaylist')
# def getVideosByPlaylist():
#     allVideosByPlaylistBuckets = []
#     try:
#         # Grab all 'Youtube' playlistResources
#         Options = {
#             'parts': ["id"]  # , "snippet"
#         }
#         playlistResource_res = sdk.YouTube().get("playlists", "/", opts=Options)
#         # To see what the response object looks like,
#         # please visit : https://developers.google.com/youtube/v3/docs/playlists#resource

#         for playlistResource in playlistResource_res["items"]:
#             Options = {
#                 'parts': ["id", "snippet"],
#                 'playlistId': playlistResource["id"]
#             }
#             playlistItems_res = sdk.YouTube().get("playlistItems", "/", opts=Options)
#             # To see what the response object looks like,
#             # please visit : https://developers.google.com/youtube/v3/docs/playlistItems

#             playlistVideoIds = [item["snippet"]["resourceId"]["videoId"]
#                                 for item in playlistItems_res['items']]

#             playlistResource["videoResources"] = []
#             for id in playlistVideoIds:

#                 Options = {
#                     'parts': ["id"],
#                     'id': id
#                 }
#                 resource = sdk.YouTube().get("videos", "/", opts=Options)['items'][0]

#                 playlistResource["videoResources"].append(resource)
#                 # To see what the response object looks like,
#                 # please visit : https://developers.google.com/youtube/v3/docs/videos#resource

#             allVideosByPlaylistBuckets.append(playlistResource)
#     except Exception:
#         raise

#     return allVideosByPlaylistBuckets
