from flask import current_app, render_template  # , redirect, abort, make_response, url_for, request
# from flask_sqlalchemy import get_debug_queries
from flask_cors import cross_origin
# from flask_login import login_required  # , current_user

from . import main_bp

# from app.api.models import User, Comment, Role, Permission  #
from app.api.services import videoService as video
# from app.api.utils.decorators import admin_required, permission_required


# @main_bp.after_app_request
# def after_request(response):
#     for query in get_debug_queries():
#         if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
#             current_app.logger.warning(
#                 'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
#                 % (query.statement, query.parameters, query.duration,
#                    query.context))
#     return response


@main_bp.route('/')
@main_bp.route('/index')
@cross_origin()
def index():
    return render_template(
        'index.html',
        videos=video.getAllVideos(),
        channelID=current_app.config['YOUTUBE_CHANNEL_ID'])


# @main_bp.route('/shutdown')
# def server_shutdown():
#     if not current_app.testing:
#         abort(404)
#     shutdown = request.environ.get('werkzeug.server.shutdown')
#     if not shutdown:
#         abort(500)
#     shutdown()
#     return 'Shutting down...'


# @main_bp.route('/moderate')
# @login_required
# @permission_required(Permission.MODERATE)
# def moderate():
#     page = request.args.get('page', 1, type=int)
#     pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
#         error_out=False)
#     comments = pagination.items
#     return render_template('moderate.html', comments=comments,
#                            pagination=pagination, page=page)


# @main_bp.route('/moderate/enable/<int:id>')
# @login_required
# @permission_required(Permission.MODERATE)
# def moderate_enable(id):
#     comment = Comment.query.get_or_404(id)
#     comment.disabled = False
#     db.session.add(comment)
#     db.session.commit()
#     return redirect(url_for('.moderate',
#                             page=request.args.get('page', 1, type=int)))


# @main_bp.route('/moderate/disable/<int:id>')
# @login_required
# @permission_required(Permission.MODERATE)
# def moderate_disable(id):
#     comment = Comment.query.get_or_404(id)
#     comment.disabled = True
#     db.session.add(comment)
#     db.session.commit()
#     return redirect(url_for('.moderate',
#                             page=request.args.get('page', 1, type=int)))
