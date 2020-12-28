from flask import Blueprint
from flask import request, jsonify

from apps.authentication.custom_authentication import authentication, create_token, KEY, TokenAuthentication
from apps.authentication.model import RevokedToken
from apps.common.custom_error import APIException
from apps.users.model import User

app_auth = Blueprint('app_auth', __name__)
auth = TokenAuthentication()


@app_auth.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = authentication(username, password)
    if not user:
        raise APIException(message='Login fail', status_code=400)

    token = create_token(user)
    return jsonify({
        'status': True,
        'message': 'Login success',
        'token': token.decode('UTF-8')
    }), 200


@app_auth.route('/logout', methods=['GET'])
@auth.token_required
def logout():
    token = request.headers[KEY]
    revoked_token = RevokedToken(token=token)
    revoked_token.save()
    return jsonify({'message': 'You are logout', 'status': True}), 200


@app_auth.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        raise APIException(message='invalid data')
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        raise APIException(message='username or email is exists')

    user = User(username=username, email=email)

    user.hash_password(password)
    user.save()

    return jsonify(
        status=True,
        message='create success',
        data=user.serializer
    )


@app_auth.route('/reset_password', methods=['POST'])
@auth.token_required
def reset_password():
    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    user = request.user

    if user.verify_password(old_password):
        if new_password == confirm_password:
            user.hash_password(new_password)
            user.save()
            return jsonify({
                'status': True,
                'message': 'Success'
            })

    raise APIException(message='invalid data')
