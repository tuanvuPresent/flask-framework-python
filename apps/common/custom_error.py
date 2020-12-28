from flask import jsonify, Blueprint

error = Blueprint('error', __name__)


class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv


@error.errorhandler(APIException)
def handle_error(e):
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response


@error.errorhandler(401)
def error_401(e):
    return jsonify(
        status=False,
        message=e.description
    )


@error.app_errorhandler(403)
def error_403(e):
    return jsonify(
        status=False,
        message=e.description
    )


@error.app_errorhandler(404)
def error_404(e):
    return jsonify(
        status=False,
        message=e.description
    )


@error.app_errorhandler(500)
def error_500(e):
    return jsonify(
        status=False,
        message=e.description
    )
