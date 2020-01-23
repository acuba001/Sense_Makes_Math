from app.errors import errors_bp as bp
from flask import request, jsonify


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


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


@bp.errorhandler(407)
def validation_error(e):
    return bad_request(e.args[0])
