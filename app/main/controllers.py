import requests
from flask import current_app

from app import cache
from app.libraries import Error, myResponse, strip_html as strip
from .sdk import YouTube
from . import sdk


blog_timeout = 60 * current_app.config['BLOGGER_DATA_FETCH_PER_DAY'] / 24

video_timeout = 60 * current_app.config['YOUTUBE_DATA_FETCH_PER_DAY'] / 24
product_timeout = 60 * current_app.config['PRINTFUL_DATA_FETCH_PER_DAY'] / 24


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
        playlist_res = YouTube().get('playlists', '/', opts=Options) or {}
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
            playlistItems_res = YouTube().get("playlistItems", "/", opts=Options)
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
            resource = YouTube().get("videos", "/", opts=Options)['items'][0]
            # To see what the response object looks like,
            # please visit : https://developers.google.com/youtube/v3/docs/videos#resource
            resource["playlistResource"] = playlistItem["playlistResource"]
            if resource not in allVideoResources:
                allVideoResources.append(resource)

    except Exception as err:
        raise Error(err)

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
            'parts': ["id", "snippet"]
        }
        playlistResource_res = YouTube().get("playlists", "/", opts=Options)
        # To see what the response object looks like,
        # please visit : https://developers.google.com/youtube/v3/docs/playlists#resource

        for playlistResource in playlistResource_res["items"]:
            Options = {
                'parts': ["id", "snippet"],
                'playlistId': playlistResource["id"]
            }
            playlistItems_res = YouTube().get("playlistItems", "/", opts=Options)
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
                resource = YouTube().get("videos", "/", opts=Options)['items'][0]

                playlistResource["videoResources"].append(resource)
                # To see what the response object looks like,
                # please visit : https://developers.google.com/youtube/v3/docs/videos#resource

            allVideosByPlaylistBuckets.append(playlistResource)
    except Exception:
        raise

    return allVideosByPlaylistBuckets


@cache.cached(timeout=product_timeout, key_prefix='getStockPrintfulCatalog')
def getStockPrintfulCatalog(WithVariants=True):
    """

    """
    controller = sdk.Printful()
    res = myResponse("printful")
    # context = inspect.stack()[0]

    errors = []
    products = []
    products_with_variants = []

    try:
        products.extend(controller.get("products"))

        if WithVariants:
            for product in products:
                product_api_url = "products/{}".format(product['id'])
                product_with_variants = controller.get(product_api_url)
                products_with_variants.append(product_with_variants)
    except Exception as err:
        errors.append(err)

    print(str(errors))

    if len(errors) > 0:
        return res.config({'code': 404, 'results': None, 'error': errors[0]})
    else:
        payload = products_with_variants if WithVariants else products
        return res.config({'code': 200, 'results': payload, 'error': None})


@cache.cached(timeout=blog_timeout, key_prefix='getBloggerData')
def getBloggerData():
    url = 'https://www.googleapis.com/blogger/v3/blogs/' + \
        current_app.config['BLOGGER_PAGE_BLOG_ID'] + '/posts'
    params = {
        'key': current_app.config['GOOGLE_API_KEY']
    }

    res = requests.get(url, params=params)
    res_items = res.json().get("items")
    coolarray = []
    for item in res_items:
        theTitle = item["title"]
        theContent = item["content"]
        post = {'title': theTitle, 'content': strip(theContent)}
        coolarray.append(post)
    return coolarray
