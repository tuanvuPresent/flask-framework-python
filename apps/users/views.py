from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api

from app import db
from apps.authentication.custom_authentication import TokenAuthentication
from apps.common.custom_error import APIException
from apps.users.model import User

app_user = Blueprint('app_user', __name__)
auth = TokenAuthentication()


class UserAPIView(Resource):
    @auth.token_required
    def get(self):
        query = User.query.all()
        data = [user.serializer for user in query]
        return jsonify(
            data=data,
            message='get all',
            status=True
        )


class UserListAPIView(Resource):
    @auth.token_required
    def get(self, pk):
        user = User.query.get(pk)
        if user:
            return jsonify(
                data=user.serializer,
                message='get user {}'.format(pk),
                status=True
            )
        raise APIException(message='Not Found', status_code=404)

    @auth.token_required
    def put(self, pk):
        data = request.json
        username = data.get('username')
        email = data.get('email')

        if User.query.filter(User.id != pk).filter_by(email=email).first() \
                or User.query.filter(User.id != pk).filter_by(username=username).first():
            raise APIException(message='username or email is exists')

        user = User.query.get(pk)
        user.username = username
        user.email = email
        user.save()
        return jsonify(
            data=user.serializer,
            message='update user {}'.format(pk),
            status=True
        )

    @auth.token_required
    def delete(self, pk):
        user = User.query.get(pk)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify(
                message='delete success',
                status=True
            )
        raise APIException(message='Not Found', status_code=404)


api = Api(app_user)
api.add_resource(UserAPIView, '/users')
api.add_resource(UserListAPIView, '/users/<int:pk>')
