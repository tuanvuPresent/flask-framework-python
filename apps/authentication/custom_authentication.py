import datetime
from functools import wraps

import jwt
from flask import request
from flask_httpauth import HTTPAuth

from apps.authentication.model import RevokedToken
from apps.common.custom_error import APIException
from apps.users.model import User

KEY = 'Token'
SECRET = 'secret'
EXPIRED_TOKEN = datetime.timedelta(minutes=60)


def authentication(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        return user


class TokenAuthentication(HTTPAuth):
    def token_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if KEY in request.headers:
                token = request.headers[KEY]

            if not token:
                raise APIException(message='Token is missing!', status_code=401)

            try:
                data = jwt.decode(token, SECRET)
                user_id = data.get('user_id', None)
                current_user = User.query.get(user_id)
                request.user = current_user
            except jwt.ExpiredSignature:
                raise APIException(message='Token is ExpiredSignature!', status_code=401)
            except:
                raise APIException(message='Token is invalid!', status_code=401)

            if is_blacklisted(token):
                raise APIException(message='You are logged out and you must login again', status_code=401)

            return f(*args, **kwargs)

        return decorated


def create_token(user):
    return jwt.encode(
        {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + EXPIRED_TOKEN
        },
        SECRET,
    )


def is_blacklisted(token):
    query = RevokedToken.query.filter_by(token=token).first()
    return bool(query)
