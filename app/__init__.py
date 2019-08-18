from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_caching import Cache

app = Flask(__name__)

app.config.from_object(Config)

bootstrap = Bootstrap(app=app)
cache = Cache(app=app, config={'CACHE_TYPE': app.config['CACHE_TYPE']})

from app.main import bp as main_bp
from app.errors import bp as errors_bp
from app.libraries import bp as libraries_bp

app.register_blueprint(main_bp)
app.register_blueprint(errors_bp)
app.register_blueprint(libraries_bp)

# =================================================================================
#  TodoList
# =================================================================================
# 1) Create a subscription
# 
#                POST {base_URL}/subscriptions?part=snippet
#                Request body:
#                {
#                    'snippet': {
#                    'resourceId': {
#                        'kind': 'youtube#channel',
#                        'channelId': 'UC_x5XG1OV2P6uZZ5FSM9Ttw' 
#                    }
#                    }
#                }
#


# =============================================================================================
#  YouTube Resources and resource types
#
# [NOTE] A resource is an individual data entity with a unique identifier. 
# The table below describes the different types of resources that you can interact with 
# using the API.
# 
# [NOTE] Note that, in many cases, a resource contains references to other resources. 
# 
# For example, 
# a playlistItem resource's snippet.resourceId.videoId property identifies a video resource
# that, in turn, contains complete information about the video. 
# 
# As another example, 
# a search result contains either a videoId, playlistId, or channelId property that 
# identifies a particular video, playlist, or channel resource.
# 
#                    
#   Resource                        Description
# ===============================================================================================
# activity	        |   Contains information about an action that a particular user has taken 
#                   |   on the YouTube site. User actions that are reported in activity feeds 
#                   |   include rating a video, sharing a video, marking a video as a favorite, 
#                   |   and posting a channel bulletin, among others.
# -----------------------------------------------------------------------------------------------
# channel	        |   Contains information about a single YouTube channel.
# -----------------------------------------------------------------------------------------------
# channelBanner	    |   Identifies the URL to use to set a newly uploaded image as the banner 
#                   |   image for a channel.
# -----------------------------------------------------------------------------------------------
# channelSection	|   Contains information about a set of videos that a channel has chosen 
#                   |   to feature. For example, a section could feature a channel's latest 
#                   |   uploads, most popular uploads, or videos from one or more playlists.
# -----------------------------------------------------------------------------------------------
# guideCategory	    |   Identifies a category that YouTube associates with channels based on 
#                   |   their content or other indicators, such as popularity. Guide categories 
#                   |   seek to organize channels in a way that makes it easier for YouTube 
#                   |   users to find the content they're looking for. While channels could be 
#                   |   associated with one or more guide categories, they are not guaranteed 
#                   |   to be in any guide categories.
# -----------------------------------------------------------------------------------------------
# i18nLanguage	    |   Identifies an application language that the YouTube website supports. 
#                   |   The application language can also be referred to as a UI language.
# -----------------------------------------------------------------------------------------------
# i18nRegion	    |   Identifies a geographic area that a YouTube user can select as the 
#                   |   preferred content region. The content region can also be referred to 
#                   |   as a content locale.
# -----------------------------------------------------------------------------------------------
# playlist	        |   Represents a single YouTube playlist. A playlist is a collection of 
#                   |   videos that can be viewed sequentially and shared with other users.
# -----------------------------------------------------------------------------------------------
# playlistItem	    |   Identifies a resource, such as a video, that is part of a playlist. 
#                   |   The playlistItem resource also contains details that explain how 
#                   |   the included resource is used in the playlist.
# ------------------------------------------------------------------------------------------------
# search result	    |   Contains information about a YouTube video, channel, or playlist 
#                   |   that matches the search parameters specified in an API request. 
#                   |   While a search result points to a uniquely identifiable resource, 
#                   |   like a video, it does not have its own persistent data.
# -------------------------------------------------------------------------------------------------
# subscription	    |   Contains information about a YouTube user subscription. A subscription 
#                   |   notifies a user when new videos are added to a channel or when another 
#                   |   user takes one of several actions on YouTube, such as uploading a video, 
#                   |   rating a video, or commenting on a video.
# -------------------------------------------------------------------------------------------------
# thumbnail	        |   Identifies thumbnail images associated with a resource.
# -------------------------------------------------------------------------------------------------
# video	            |   Represents a single YouTube video.
# -------------------------------------------------------------------------------------------------
# videoCategory	    |   Identifies a category that has been or could be associated with uploaded 
#                   |   videos.
# -------------------------------------------------------------------------------------------------
# watermark	        |   Identifies an image that displays during playbacks of a specified 
#                   |   channel's videos. The channel owner can also specify a target 
#                   |   channel to which the image links as well as timing details that 
#                   |   determine when the watermark appears during video playbacks and 
#                   |   then length of time it is visible.
# -------------------------------------------------------------------------------------------------


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


# ================================================================
# Factors to Help Calculate Quota Usage of YouTube Resources
#  
#  
# [NOTE] Google calculates your quota usage by assigning a cost to 
# each request, but the cost is not the same for each request. Two 
# primary factors influence a request's quota cost:
#
#   Factors
# ================================================================
# [1] Different types of operations have different quota costs.
#       | --------------------------------------------------------
#       |   A simple read operation that only retrieves the ID of 
#       |   each returned resource has a cost of approximately 1 
#       |   unit.
#       | --------------------------------------------------------
#       |   A write operation has a cost of approximately 50 units.
#       | --------------------------------------------------------
#       |   A video upload has a cost of approximately 1600 units.
#       | --------------------------------------------------------
# 
# [2, a] Read and write operations use different amounts of quota 
# depending on the number of resource parts that each request 
# retrieves. Note that insert and update operations write data and 
# also return a resource. So, for example, inserting a playlist has 
# a quota cost of 50 units for the write operation plus the cost of 
# the returned playlist resource.
#
# [2, b] Each API resource is divided into parts. Each part contains a 
# group of related properties, and the groups are designed so that your 
# application only needs to retrieve the types of data that it actually 
# uses.
#
# [2, c] An API request that returns resource data must specify the 
# resource parts that the request retrieves. Each part then adds 
# approximately 2 units to the request's quota cost. As such, a 
# videos.list request that only retrieves the snippet part for each 
# video might have a cost of 3 units. However, a videos.list request 
# that retrieves all of the parts for each resource might have a cost 
# of around 21 quota units.
# --------------------------------------------------------------------------


# ===============================================================================
# Examples of Computing YouTube Route Quotas
#
#
# [NOTE] With these rules in mind, you can estimate the number of read, write, 
# or upload requests that your application could send per day without 
# exceeding your quota. 
# 
# For example, 
# if you have a daily quota of 1,000,000 units, your application could have any 
# of the following approximate limits:
# ===============================================================================
#   Ex1     |   200,000 read operations that each retrieve two resource parts.
# -------------------------------------------------------------------------------
#   Ex2     |   10,000 write operations and 90,000 additional read operations 
#           |   that each retrieve two resource parts.
# -------------------------------------------------------------------------------
#   Ex3     |   400 video uploads, 1500 write operations, and 50,000 read 
#           |   operations that each retrieve two resource parts.
# -------------------------------------------------------------------------------

# Examples of paths with which to make Blogger API calls
#
# https://www.googleapis.com/blogger/v3/users/userId
# https://www.googleapis.com/blogger/v3/users/self
# https://www.googleapis.com/blogger/v3/users/userId/blogs
# https://www.googleapis.com/blogger/v3/users/self/blogs
# https://www.googleapis.com/blogger/v3/blogs/blogId
# https://www.googleapis.com/blogger/v3/blogs/byurl
# https://www.googleapis.com/blogger/v3/blogs/blogId/posts
# https://www.googleapis.com/blogger/v3/blogs/blogId/posts/bypath
# https://www.googleapis.com/blogger/v3/blogs/blogId/posts/search
# https://www.googleapis.com/blogger/v3/blogs/blogId/posts/postId
# https://www.googleapis.com/blogger/v3/blogs/blogId/posts/postId/comments
# https://www.googleapis.com/blogger/v3/blogs/blogId/posts/postId/comments/commentId
# https://www.googleapis.com/blogger/v3/blogs/blogId/pages
# https://www.googleapis.com/blogger/v3/blogs/blogId/pages/pageId


# =====================================================
# [NOTE] In app.init.py (i.e. this file)...
#
#   Example 1
# =====================================================
# from flask import Flask
# from yourapplication.simple_page import simple_page
#
# app = Flask(__name__)
# app.register_blueprint(simple_page)
#
# ------------------------------------------------------


# ======================================================
# [NOTE] In app.<component>.init.py...
# 
# Components are captured in a Blueprint and 
# are usable throughout the app. For example,  errors, 
# libraries, main.
#
#   Example 2
# ======================================================
# from flask import Blueprint
# 
# simple_page = Blueprint('simple_page', __name__,
#                         template_folder='templates')
#
# -------------------------------------------------------


# =======================================================
# [NOTE] In app.main.routes.py...
# 
#   Example 3
# =======================================================
# from flask import render_template, abort
# from jinja2 import TemplateNotFound
#
# @simple_page.route('/', defaults={'page': 'index'})
# @simple_page.route('/<page>')
# def show(page):
#     try:
#         return render_template('pages/%s.html' % page)
#     except TemplateNotFound:
#         abort(404)
#
# --------------------------------------------------------

