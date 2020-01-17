from app.main import main_bp as bp
from .controllers.youtube import getAllYouTubeVideos, getLatestYouTubeVideo, getYouTubeVideosByPlaylist
from .controllers.blogger import getBloggerData
from .controllers.printful import getStockPrintfulCatalog
from flask import current_app, render_template, jsonify
from flask_cors import cross_origin


@bp.route('/')
@bp.route('/index')
@cross_origin()
def index():
    return render_template(
        'index.html',
        videos=getAllYouTubeVideos(),
        channelID=current_app.config['YOUTUBE_CHANNEL_ID']
    )


@bp.route('/yt-posts')
@cross_origin()
def ytPosts():
    posts = getAllYouTubeVideos()
    return jsonify({'posts': posts})


@bp.route('/yt-posts/latest')
@cross_origin()
def ytPostsLatest():
    posts = getLatestYouTubeVideo()
    return jsonify({'posts': posts})


@bp.route('/yt-posts/playlist')
@cross_origin()
def ytPostsByPlaylist():
    posts = getYouTubeVideosByPlaylist()
    return jsonify({'posts': posts})


@bp.route('/blog-posts')
@cross_origin()
def blogPosts():
    posts = getBloggerData()
    return jsonify({'posts': posts})


@bp.route('/store/catalog')
@cross_origin()
def stockPrintfulProducts():
    catalog = getStockPrintfulCatalog(False)
    return jsonify(catalog)
