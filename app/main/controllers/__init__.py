from flask import current_app, request
from abc import ABC, abstractmethod
import inspect

from app.errors import Error, InternalServerError


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
            raise Error(None, inspect.stack()[0])
        #
        # step 2: Load The Endpoint
        if endpoint:
            url += endpoint

        # Configure the request parameters
        #
        # Step 1: Load Hidden Values
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
        for field in opts.keys():
            if field == 'parts':
                for part in opts["parts"]:
                    if self.isValidPart(part):
                        if part == 'id':
                            continue
                        params['part'] += ", "+part
            elif field is "pageToken":
                params["pageToken"] = opts["pageToken"]
            elif field is "publishedAfter":
                params["publishedAfter"] = opts["publishedAfter"]
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
            elif field is 'hl':
                params['hl'] = opts['hl']
            elif field is 'maxHeight':
                params['maxHeight'] = opts['maxHeight']
            elif field is 'maxResults':
                params['maxResults'] = opts['maxResults']
            elif field is 'maxWidth':
                params['maxWidth'] = opts['maxWidth']
            elif field is 'onBehalfOfContentOwner':
                params['onBehalfOfContentOwner'] = opts['onBehalfOfContentOwner']
            elif field is 'onBehalfOfContentOwnerChannel':
                params['onBehalfOfContentOwnerChannel'] = opts['onBehalfOfContentOwnerChannel']
            elif field is 'videoCategoryId':
                params['videoCategoryId'] = opts['videoCategoryId']

        # Make a call to the YouTubeData Api.V3
        try:
            xRes = request.get(url, params=params)
            # To see what a response object might look like,
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


class PrintfulController(XApiController):
    """
    Please See: https://www.printful.com/docs/ for
    further details ont he Printful Api
    """

    def __init__(self):
        self.base_url = 'https://api.printful.com/{}'

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
        url = self.base_url.format(str(endpoint))
        # else:
        #     raise BadUrlError(url, None, context)

        # Load params
        params = {
            'Authorization': current_app.config['PRINTFUL_API_KEY']
        }

        # Make call to 'Printful' api
        xRes = request.get(url, params=params).json()

        if xRes["code"] in [200]:
            # Return formated response
            return xRes["result"]
        else:
            raise InternalServerError(None, context, "printful", url)

    def post(self, Resource):
        pass
