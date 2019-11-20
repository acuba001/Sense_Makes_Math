from app.errors import errors_bp as bp
from flask import render_template, request, jsonify
from app import db


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found_error(error):
    # if wants_json_response():
    #     return api_error_response(404)
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    # if wants_json_response():
    #     return api_error_response(500)
    return render_template('errors/500.html'), 500


@bp.app_errorhandler(400)
def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


@bp.app_errorhandler(401)
def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


@bp.app_errorhandler(403)
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


# @api.errorhandler(ValidationError)
# def validation_error(e):
#     return bad_request(e.args[0])
