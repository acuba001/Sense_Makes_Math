from app.main import bp
from app.main.youtube import getAllYouTubeVideos
from app.main.facebook import getFacebookPosts
from app.main.blogger import getBloggerData
from flask import current_app, render_template, jsonify, abort
from flask_cors import cross_origin

@bp.route('/')
@bp.route('/index')
@cross_origin()
def index():
    return render_template(
        'index.html', 
        videos=getAllYouTubeVideos(), 
        channelID=current_app.config['YOUTUBE_CHANNEL_ID'],
        fbAppId=current_app.config['FACEBOOK_APP_ID'],
        fbAppVer=current_app.config['FACEBOOK_API_VERSION']
    )

@bp.route('/fb-posts')
@cross_origin()
def fbPosts():
    posts = getFacebookPosts()
    return jsonify({'posts': posts})
 
@bp.route('/yt-posts')
@cross_origin()
def ytPosts():
    posts = getAllYouTubeVideos()
    return jsonify({'posts': posts})
    
@bp.route('/blog-posts')
@cross_origin()
def blogPosts():
	posts = getBloggerData()	
	return jsonify({'posts': posts})
