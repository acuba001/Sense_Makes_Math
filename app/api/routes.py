from flask import jsonify
from flask_cors import cross_origin
from .controllers.youtube import getAllVideos, getLatestVideo, getVideosByPlaylist
from .controllers.printful import getStockPrintfulCatalog
from .controllers.blogger import getBloggerData
from app.api import api_bp


@api_bp.route('/yt-posts')
@cross_origin()
def ytPosts():
    posts = getAllVideos()
    return jsonify({'posts': posts})


@api_bp.route('/yt-posts/latest')
@cross_origin()
def ytPostsLatest():
    posts = getLatestVideo()
    return jsonify({'posts': posts})


@api_bp.route('/yt-posts/playlist')
@cross_origin()
def ytPostsByPlaylist():
    posts = getVideosByPlaylist()
    return jsonify({'posts': posts})


@api_bp.route('/blog-posts')
@cross_origin()
def blogPosts():
    posts = getBloggerData()
    return jsonify({'posts': posts})


@api_bp.route('/store/catalog')
@cross_origin()
def stockPrintfulProducts():
    catalog = getStockPrintfulCatalog(False)
    return jsonify(catalog)