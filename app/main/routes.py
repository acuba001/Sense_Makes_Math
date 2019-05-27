from app.main import bp
from app.main.youtube import getYouTubeData
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
        'fb_9p;posts.html',
        posts = getFacebookPosts(),
        pageId = current_app.config['FACEBOOK_PAGE_ID']
        )