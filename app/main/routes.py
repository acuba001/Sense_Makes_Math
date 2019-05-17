from app.main import bp
from app.main.youtube import getYouTubeData
from flask import render_template

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', videos=getYouTubeData())