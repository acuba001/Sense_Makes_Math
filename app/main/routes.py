from app.main import bp
from app.main.youtube import getYouTubeData
from flask import current_app, render_template

@bp.route('/')
@bp.route('/index')
def index():
    return render_template(
        'index.html', 
        videos=getYouTubeData(), 
        channelID=current_app.config['YOUTUBE_CHANNEL_ID']
    )