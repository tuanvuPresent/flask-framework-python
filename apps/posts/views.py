from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api

from app import db
from apps.authentication.custom_authentication import TokenAuthentication
from apps.common.custom_error import APIException
from apps.posts.model import Category, Post

app_post = Blueprint('app_post', __name__)
auth = TokenAuthentication()


class PostAPIView(Resource):

    @auth.token_required
    def post(self):
        data = request.json
        title = data.get('title')
        body = data.get('body')
        category_name = data.get('category_name')

        if not title or not body or not category_name:
            raise APIException(message='invalid')

        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            category.save()
        category_id = category.id
        post = Post(
            title=title,
            body=body,
            category_id=category_id,
            user_id=request.user.id
        )
        post.save()
        return jsonify(
            data=post.serializer,
            message='create success',
            status=True
        )

    @auth.token_required
    def get(self):
        query = Post.query.all()
        data = ([post.serializer for post in query])
        return jsonify(
            message='get all',
            status=True,
            data=data
        )


class DetailPostAPIView(Resource):
    @auth.token_required
    def get(self, pk):
        post = Post.query.filter_by(id=pk).first()
        if post:
            return jsonify(
                message='get',
                status=True,
                data=post.serializer
            )
        raise APIException(message='Not Found', status_code=404)

    @auth.token_required
    def put(self, pk):
        post = Post.query.get(pk)
        if post:
            data = request.json
            title = data.get('title')
            body = data.get('body')
            category_name = data.get('category_name')

            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                category.save()
            category_id = category.id

            post.title = title
            post.body = body
            post.category_id = category_id

            post.save()

            return jsonify(
                message='update',
                status=True,
                data=post.serializer
            )
        raise APIException(message='Not Found', status_code=404)

    @auth.token_required
    def delete(self, pk):
        post = Post.query.get(pk)
        if post:
            db.session.delete(post)
            db.session.commit()
            return jsonify({
                'status': True,
                'message': 'Delete success'
            })
        raise APIException(message='Not Found', status_code=404)


api = Api(app_post)
api.add_resource(PostAPIView, '/posts')
api.add_resource(DetailPostAPIView, '/posts/<int:pk>')
