import inspect
import requests
# import json
from abc import ABC, abstractmethod
from flask import current_app
from . import Error


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

    [NOTE] A resource is an individual data entity with a unique identifier.
    The table below describes the different types of resources that you can interact with
    using the API.

    [NOTE] Note that, in many cases, a resource contains references to other resources.

    For example,
    a playlistItem resource's snippet.resourceId.videoId property identifies a video resource
    that, in turn, contains complete information about the video.

    As another example,
    a search result contains either a videoId, playlistId, or channelId property that
    identifies a particular video, playlist, or channel resource.


    Resource                        Description
    ===============================================================================================
    activity	        |   Contains information about an action that a particular user has taken
                    |   on the YouTube site. User actions that are reported in activity feeds
                    |   include rating a video, sharing a video, marking a video as a favorite,
                    |   and posting a channel bulletin, among others.
    -----------------------------------------------------------------------------------------------
    channel	        |   Contains information about a single YouTube channel.
    -----------------------------------------------------------------------------------------------
    channelBanner	    |   Identifies the URL to use to set a newly uploaded image as the banner
                    |   image for a channel.
    -----------------------------------------------------------------------------------------------
    channelSection	|   Contains information about a set of videos that a channel has chosen
                    |   to feature. For example, a section could feature a channel's latest
                    |   uploads, most popular uploads, or videos from one or more playlists.
    -----------------------------------------------------------------------------------------------
    guideCategory	    |   Identifies a category that YouTube associates with channels based on
                    |   their content or other indicators, such as popularity. Guide categories
                    |   seek to organize channels in a way that makes it easier for YouTube
                    |   users to find the content they're looking for. While channels could be
                    |   associated with one or more guide categories, they are not guaranteed
                    |   to be in any guide categories.
    -----------------------------------------------------------------------------------------------
    i18nLanguage	    |   Identifies an application language that the YouTube website supports.
                    |   The application language can also be referred to as a UI language.
    -----------------------------------------------------------------------------------------------
    i18nRegion	    |   Identifies a geographic area that a YouTube user can select as the
                    |   preferred content region. The content region can also be referred to
                    |   as a content locale.
    -----------------------------------------------------------------------------------------------
    playlist	        |   Represents a single YouTube playlist. A playlist is a collection of
                    |   videos that can be viewed sequentially and shared with other users.
    -----------------------------------------------------------------------------------------------
    playlistItem	    |   Identifies a resource, such as a video, that is part of a playlist.
                    |   The playlistItem resource also contains details that explain how
                    |   the included resource is used in the playlist.
    ------------------------------------------------------------------------------------------------
    search result	    |   Contains information about a YouTube video, channel, or playlist
                    |   that matches the search parameters specified in an API request.
                    |   While a search result points to a uniquely identifiable resource,
                    |   like a video, it does not have its own persistent data.
    -------------------------------------------------------------------------------------------------
    subscription	    |   Contains information about a YouTube user subscription. A subscription
                    |   notifies a user when new videos are added to a channel or when another
                    |   user takes one of several actions on YouTube, such as uploading a video,
                    |   rating a video, or commenting on a video.
    -------------------------------------------------------------------------------------------------
    thumbnail	        |   Identifies thumbnail images associated with a resource.
    -------------------------------------------------------------------------------------------------
    video	            |   Represents a single YouTube video.
    -------------------------------------------------------------------------------------------------
    videoCategory	    |   Identifies a category that has been or could be associated with uploaded
                    |   videos.
    -------------------------------------------------------------------------------------------------
    watermark	        |   Identifies an image that displays during playbacks of a specified
                    |   channel's videos. The channel owner can also specify a target
                    |   channel to which the image links as well as timing details that
                    |   determine when the watermark appears during video playbacks and
                    |   then length of time it is visible.
    -------------------------------------------------------------------------------------------------


    ====================================================================================
    Basic Operations on YouTube Resources

    Operation                    Description
    ====================================================================================
    list	        |   Retrieves (GET) a list of zero or more resources.
    ------------------------------------------------------------------------------------
    insert	    |   Creates (POST) a new resource.
    ------------------------------------------------------------------------------------
    update	    |   Modifies (PUT) an existing resource to reflect data in your request.
    ------------------------------------------------------------------------------------
    delete	    |   Removes (DELETE) a specific resource.
    -------------------------------------------------------------------------------------


    =================================================================
    Supported Operations on YouTube Resources

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

    ================================================================
    Factors to Help Calculate Quota Usage of YouTube Resources


    [NOTE] Google calculates your quota usage by assigning a cost to
    each request, but the cost is not the same for each request. Two
    primary factors influence a request's quota cost:

    Factors
    ================================================================
    [1] Different types of operations have different quota costs.
        | --------------------------------------------------------
        |   A simple read operation that only retrieves the ID of
        |   each returned resource has a cost of approximately 1
        |   unit.
        | --------------------------------------------------------
        |   A write operation has a cost of approximately 50 units.
        | --------------------------------------------------------
        |   A video upload has a cost of approximately 1600 units.
        | --------------------------------------------------------

    [2, a] Read and write operations use different amounts of quota
    depending on the number of resource parts that each request
    retrieves. Note that insert and update operations write data and
    also return a resource. So, for example, inserting a playlist has
    a quota cost of 50 units for the write operation plus the cost of
    the returned playlist resource.

    [2, b] Each API resource is divided into parts. Each part contains a
    group of related properties, and the groups are designed so that your
    application only needs to retrieve the types of data that it actually
    uses.

    [2, c] An API request that returns resource data must specify the
    resource parts that the request retrieves. Each part then adds
    approximately 2 units to the request's quota cost. As such, a
    videos.list request that only retrieves the snippet part for each
    video might have a cost of 3 units. However, a videos.list request
    that retrieves all of the parts for each resource might have a cost
    of around 21 quota units.
    --------------------------------------------------------------------------
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
            url = self.base_url + resource_name
        else:
            raise  # Error(None, inspect.stack()[0])
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
        for field in opts.keys():
            if field in optional_params:
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
                return xRes.json()
            else:
                raise Error("[{} LN {}] YouTubeError(" + str(xRes.status_code) + "): " + xRes.message, inspect.stack()[0], 'YouTube', url)
        except Exception as err:
            raise Error("[{} {}] InternalServerError: " + str(err), inspect.stack()[0])

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
    timeout = 60 * current_app.config['PRINTFUL_DATA_FETCH_PER_DAY'] / 24

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


class Paypal(XApiController):
    """
    Please See: https://www.printful.com/docs/ for
    further details ont he Printful Api
    """

    _base_url = 'https://api.printful.com/{}'
    timeout = 60 * current_app.config['PRINTFUL_DATA_FETCH_PER_DAY'] / 24

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
