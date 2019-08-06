from app.main import bp
from app.main.youtube import getAllYouTubeVideos
from app.main.facebook import getFacebookPosts
from app.main.blogger import getBloggerData
from flask import current_app, render_template, jsonify, abort


@bp.route('/')
@bp.route('/index')
def index():
    return render_template(
        'index.html', 
        videos=getAllYouTubeVideos(), 
        channelID=current_app.config['YOUTUBE_CHANNEL_ID'],
        fbAppId=current_app.config['FACEBOOK_APP_ID'],
        fbAppVer=current_app.config['FACEBOOK_API_VERSION']
    )

# @bp.route()
@bp.route('/fb-posts')
def fbPosts():
    posts = getFacebookPosts()
    return jsonify({'posts': posts})
 
@bp.route('/yt-posts')
def ytPosts():
    # Real Sample of post 
    # {
    #   "etag": "\"Bdx4f4ps3xCOOo1WZ91nTLkRZ_c/3W8Ro0CnpzXIr0qcQ4b6nJvBqdQ\"", 
    #   "id": "5quyA4w_tV8", 
    #   "kind": "youtube#video", 
    #   "player": {
    #     "embedHtml": "<iframe width=\"480\" height=\"270\" src=\"//www.youtube.com/embed/5quyA4w_tV8\" frameborder=\"0\" allow=\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>"
    #   }
    # }
    posts = getAllYouTubeVideos()
    return jsonify({'posts': posts})
    
@bp.route('/blog-posts')
def blogPosts():
	posts = getBloggerData()	
	return jsonify({'posts': posts})
