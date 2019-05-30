from app.main import bp
from app.main.youtube import getYouTubeData
from app.main.facebook import getFacebookPosts
from flask import current_app, render_template 

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
    return render_template(
        '_posts1415.html',
        posts = getFacebookPosts(),
        pageId = current_app.config['FACEBOOK_PAGE_ID']
        )
    
@bp.route('/yt-posts')
def ytPosts():
    return render_template(
        '_video.html',
        posts = getYouTubeData(),
        channelID=current_app.config['YOUTUBE_CHANNEL_ID']
        )

