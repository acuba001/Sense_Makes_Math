from app.main import bp
from app.main.youtube import getYouTubeData
from app.main.facebook import getFacebookPosts
from app.main.blogger import getBloggerData
from flask import current_app, render_template, jsonify

@bp.route('/')
@bp.route('/index')
def index():
    return render_template(
        'index.html', 
        videos=getYouTubeData(), 
        channelID=current_app.config['YOUTUBE_CHANNEL_ID'],
        fbAppId=current_app.config['FACEBOOK_APP_ID'],
        fbAppVer=current_app.config['FACEBOOK_API_VERSION']
    )

@bp.route('/fb-posts')
def fbPosts():
    posts = getFacebookPosts()
    return jsonify(posts)

@bp.route('/yt-posts')
def ytPosts():
	return render_template(
        '_video.html',
        posts = getYouTubeData(),
        channelID=current_app.config['YOUTUBE_CHANNEL_ID']
        )

@bp.route('/blog-posts')
def blogPosts():
	return jsonify({'blog_posts': getBloggerData()})
