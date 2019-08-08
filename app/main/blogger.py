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

from app import app, cache
from app.libraries import strip_html as strip

import json
import requests

timeout = 60*app.config['BLOGGER_DATA_FETCH_PER_DAY']/24

@cache.cached(timeout=timeout, key_prefix='getBloggerData')
def getBloggerData():
    url = 'https://www.googleapis.com/blogger/v3/blogs/' + \
        app.config['BLOGGER_PAGE_BLOG_ID'] + '/posts'
    params = {
        'key': app.config['GOOGLE_API_KEY']
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

# [TODO] Create a subscription
# 
# POST {base_URL}/subscriptions?part=snippet
#  Request body:
#   {
#     'snippet': {
#       'resourceId': {
#         'kind': 'youtube#channel',
#         'channelId': 'UC_x5XG1OV2P6uZZ5FSM9Ttw' 
#        }
#      }
#   }



