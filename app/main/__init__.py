from flask import Blueprint, current_app, render_template, jsonify
from flask_cors import cross_origin
from app.api.models import Permission
from .controllers import getAllVideos, getLatestVideo, getVideosByPlaylist, getBloggerData, getStockPrintfulCatalog

main_bp = Blueprint('main', __name__, template_folder='./templates')


@main_bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@main_bp.route('/')
@main_bp.route('/index')
@cross_origin()
def index():
    return render_template(
        'index.html',
        videos=getAllVideos(),
        channelID=current_app.config['YOUTUBE_CHANNEL_ID']
    )


@main_bp.route('/yt-posts')
@cross_origin()
def ytPosts():
    posts = getAllVideos()
    return jsonify({'posts': posts})


@main_bp.route('/yt-posts/latest')
@cross_origin()
def ytPostsLatest():
    posts = getLatestVideo()
    return jsonify({'posts': posts})


@main_bp.route('/yt-posts/playlist')
@cross_origin()
def ytPostsByPlaylist():
    posts = getVideosByPlaylist()
    return jsonify({'posts': posts})


@main_bp.route('/blog-posts')
@cross_origin()
def blogPosts():
    posts = getBloggerData()
    return jsonify({'posts': posts})


@main_bp.route('/store/catalog')
@cross_origin()
def stockPrintfulProducts():
    catalog = getStockPrintfulCatalog(False)
    return jsonify(catalog)
