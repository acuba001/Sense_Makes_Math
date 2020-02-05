from flask import jsonify, request, abort, g, url_for, current_app, render_template
from flask_cors import cross_origin

from app import db
from . import api_bp
from .models import User
from .services import videoService as video, productService as prod, blogService as blog


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@api_bp.route('/')
@cross_origin()
def index():
    return render_template(
        'index.html',
        videos=video.getAllVideos(),
        channelID=current_app.config['YOUTUBE_CHANNEL_ID'])


@api_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api_bp.route('/users', methods=['GET'])
def get_users():
    # page = request.args.get('page', 1, type=int)
    # per_page = min(request.args.get('per_page', 10, type=int), 100)
    users = User.query.all()
    data = {"users": [user.to_dict() for user in users]}  # User.query, page, per_page, 'api.v1.get_users'
    return jsonify(data)


@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@api_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    if g.current_user.id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


@api_bp.route('/yt-posts')
@cross_origin()
def ytPosts():
    # data = request.get_json()
    posts = video.getAllVideos()
    return jsonify({'posts': posts})


@api_bp.route('/yt-posts/latest')
@cross_origin()
def ytPostsLatest():
    posts = video.getLatestVideo()
    return jsonify({'posts': posts})


@api_bp.route('/yt-posts/playlist')
@cross_origin()
def ytPostsByPlaylist():
    posts = video.getVideosByPlaylist()
    return jsonify({'posts': posts})


@api_bp.route('/blog-posts')
@cross_origin()
def blogPosts():
    posts = blog.getBloggerData()
    return jsonify({'posts': posts})


@api_bp.route('/store/catalog')
@cross_origin()
def stockPrintfulProducts():
    catalog = prod.getStockPrintfulCatalog(False)
    return jsonify(catalog)


# @api_bp.errorhandler(407)
# def handle_bad_request(e):
#     return 'e: ' + str(e), 407


@api_bp.app_errorhandler(400)
def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


@api_bp.app_errorhandler(401)
def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


@api_bp.app_errorhandler(403)
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


# @api_bp.errorhandler(407)
# def validation_error(e):
#     return bad_request(e.args[0])
