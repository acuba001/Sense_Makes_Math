import inspect
import requests
from flask import current_app
from abc import ABC, abstractmethod
from app.api.errors import Error


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
    =============================================================================================
    YouTube Resources and resource types

    Resource                        Description
    ===============================================================================================
    activity	    |   Contains information about an action that a particular user has taken
                    |   on the YouTube site. User actions that are reported in activity feeds
                    |   include rating a video, sharing a video, marking a video as a favorite,
                    |   and posting a channel bulletin, among others.
    -----------------------------------------------------------------------------------------------
    channel	        |   Contains information about a single YouTube channel.
    -----------------------------------------------------------------------------------------------
    channelBanner	|   Identifies the URL to use to set a newly uploaded image as the banner
                    |   image for a channel.
    -----------------------------------------------------------------------------------------------
    channelSection	|   Contains information about a set of videos that a channel has chosen
                    |   to feature. For example, a section could feature a channel's latest
                    |   uploads, most popular uploads, or videos from one or more playlists.
    -----------------------------------------------------------------------------------------------
    guideCategory	|   Identifies a category that YouTube associates with channels based on
                    |   their content or other indicators, such as popularity. Guide categories
                    |   seek to organize channels in a way that makes it easier for YouTube
                    |   users to find the content they're looking for. While channels could be
                    |   associated with one or more guide categories, they are not guaranteed
                    |   to be in any guide categories.
    -----------------------------------------------------------------------------------------------
    i18nLanguage	|   Identifies an application language that the YouTube website supports.
                    |   The application language can also be referred to as a UI language.
    -----------------------------------------------------------------------------------------------
    i18nRegion	    |   Identifies a geographic area that a YouTube user can select as the
                    |   preferred content region. The content region can also be referred to
                    |   as a content locale.
    -----------------------------------------------------------------------------------------------
    playlist	    |   Represents a single YouTube playlist. A playlist is a collection of
                    |   videos that can be viewed sequentially and shared with other users.
    -----------------------------------------------------------------------------------------------
    playlistItem	|   Identifies a resource, such as a video, that is part of a playlist.
                    |   The playlistItem resource also contains details that explain how
                    |   the included resource is used in the playlist.
    ------------------------------------------------------------------------------------------------
    search result	|   Contains information about a YouTube video, channel, or playlist
                    |   that matches the search parameters specified in an API request.
                    |   While a search result points to a uniquely identifiable resource,
                    |   like a video, it does not have its own persistent data.
    -------------------------------------------------------------------------------------------------
    subscription	|   Contains information about a YouTube user subscription. A subscription
                    |   notifies a user when new videos are added to a channel or when another
                    |   user takes one of several actions on YouTube, such as uploading a video,
                    |   rating a video, or commenting on a video.
    -------------------------------------------------------------------------------------------------
    thumbnail	    |   Identifies thumbnail images associated with a resource.
    -------------------------------------------------------------------------------------------------
    video	        |   Represents a single YouTube video.
    -------------------------------------------------------------------------------------------------
    videoCategory	|   Identifies a category that has been or could be associated with uploaded
                    |   videos.
    -------------------------------------------------------------------------------------------------
    watermark	    |   Identifies an image that displays during playbacks of a specified
                    |   channel's videos. The channel owner can also specify a target
                    |   channel to which the image links as well as timing details that
                    |   determine when the watermark appears during video playbacks and
                    |   then length of time it is visible.
    -------------------------------------------------------------------------------------------------

    =================================================================
    Supported Operations on YouTube Resources

    Operation                    Description
    ====================================================================================
    list	        |   Retrieves (GET) a list of zero or more resources.
    ------------------------------------------------------------------------------------
    insert	        |   Creates (POST) a new resource.
    ------------------------------------------------------------------------------------
    update	        |   Modifies (PUT) an existing resource to reflect data in your request.
    ------------------------------------------------------------------------------------
    delete	        |   Removes (DELETE) a specific resource.
    -------------------------------------------------------------------------------------

    Resource            list        insert      update      delete
    =================================================================
    activity            |   true    |   true    |   false   |   false
    caption			    |   true    |   true    |   true    |   true
    channel             |   true    |   false   |   false   |   false
    channelBanner		|   false   |   true    |   false   |   false
    channelSection	    |   true    |   true    |   true    |   true
    comment		        |   true    |   true    |   true    |   true
    commentThread		|   true    |   true    |   true    |   false
    guideCategory		|   true    |   false   |   false   |   false
    i18nLanguage		|   true    |   false   |   false   |   false
    i18nRegion		    |   true    |   false   |   false   |   false
    playlist			|   true    |   true    |   true    |   true
    playlistItem		|   true    |   true    |   true    |   true
    search result		|   true    |   false   |   false   |   false
    subscription		|   true    |   false   |   false   |   false
    thumbnail			|   false   |   false   |   false   |   false
    video				|   true    |   true    |   true    |   true
    videoCategory		|   true    |   false   |   false   |   false
    watermark			|   false   |   false   |   false   |   false
    ----------------------------------------------------------------
 """
    _base_url = "https://www.googleapis.com/youtube/v3/"

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, newUrl):
        if isinstance(newUrl, ""):
            self._base_url = newUrl

    @staticmethod
    def isValidPart(part):
        valid_youtube_part = [
            "contentDetails",
            "fileDetails",
            "id",
            "liveStreamingDetails",
            "localizations",
            "player",
            "processingDetails",
            "recordingDetails",
            "snippet",
            "statistics",
            "status",
            "suggestions",
            "topicDetails"
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

    @staticmethod
    def isValidParamField(field):
        optional_params = [
            'hl',
            'id',
            'maxHeight',
            'maxResults',
            'maxWidth',
            'onBehalfOfContentOwner',
            'onBehalfOfContentOwnerChannel',
            'parts',
            'pageToken',
            'playlistId',
            'publishedAfter',
            'publishedBefore',
            'regionCode',
            'videoId',
            'videoCategoryId'
        ]
        return field in optional_params

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, resource_name, endpoint, opts=None):
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
            url = self.base_url + resource_name
        else:
            raise Error(None, inspect.stack()[0])
        #
        # step 2: Load The Endpoint
        if endpoint:
            url += endpoint

        # Configure the request parameters
        #
        # Step 1: Load Configuration Values
        params = {
            'key': current_app.config['GOOGLE_API_KEY'],
            'channelId': current_app.config['YOUTUBE_CHANNEL_ID'],
            'maxResults': current_app.config['YOUTUBE_DATA_MAXRESULTS'],
            'part': 'id'
        }
        #
        # Step 2: Load a filter
        if isinstance(opts, object):
            if "chart" in opts.keys():
                params["chart"] = opts["chart"]
            elif "id" in opts.keys():
                params["id"] = opts["id"]
            elif "myRating" in opts.keys():
                params["myRating"] = opts["myRating"]
            elif "mine" in opts.keys():
                params["mine"] = opts["mine"]
            elif "playlistId" in opts.keys():
                params["minplaylistIde"] = opts["playlistId"]
            #
            # Step 3: Load Possible Optional Parameters
            for field in opts.keys():
                if self.isValidParamField(field):
                    if field == 'parts':
                        for part in opts["parts"]:
                            if self.isValidPart(part):
                                if part == 'id':
                                    continue
                                params['part'] += ", " + part
                    else:
                        params[field] = opts[field]
        #
        # Step 4: Make a call to the YouTubeData Api.V3
        try:
            xRes = requests.get(url, params=params)
            # To see what a response object might look like,
            # please visit : https://developers.google.com/youtube/v3/docs/playlists#resource or
            # in general: "https://developers.google.com/youtube/v3/docs/< valid#resource >"
            if xRes.ok:
                return xRes.json(), self.video_timeout
            else:
                raise Error(
                    template="[{} {}] YouTubeError(" + str(xRes.status_code) + ") [in {}.{}]",
                    context=inspect.stack()[0]
                )
        except Exception:
            raise  # Error("[{} {}] InternalServerError: " + str(err), inspect.stack()[0])

    def post(self, endpoint):
        pass

    def put(self, endpoint):
        pass

    def delete(self, endpoint):
        pass


class Printful(XApiController):
    """
    Please See: https://www.printful.com/docs/ for
    further details ont he Printful Api
    """

    _base_url = 'https://api.printful.com/{}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def isValid(self, endpoint):

        valid_printful_resources = [
            'products',
            'store/products',
            'orders',
            'files',
            'shipping/rates',
            'countries',
            'tax/countries',
            'tax/rates'
        ]
        return endpoint in valid_printful_resources

    def get(self, endpoint):
        context = inspect.stack()[0]

        # Create url
        #
        # [WIP] This current only works with base endpoints.
        # We need to expand the 'isValid' function to deal with
        # other cases
        #
        # if self.isValid(endpoint):
        url = self._base_url.format(str(endpoint))
        # else:
        #     raise BadUrlError(url, None, context)

        # Load params
        params = {
            'Authorization': current_app.config['PRINTFUL_API_KEY']
        }

        # Make call to 'Printful' api
        xRes = requests.get(url, params=params).json()

        if xRes["code"] in [200]:
            # Return formated response
            return xRes["result"]
        else:
            raise Error(None, context, "printful", url)

    def post(self, Resource):
        pass


# class Paypal(XApiController):
#     """
#     Please See: https://www.printful.com/docs/ for
#     further details ont he Printful Api
#     """

#     _base_url = 'https://api.printful.com/{}'
#     timeout = 60 * current_app.config['PRINTFUL_DATA_FETCH_PER_DAY'] / 24

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
