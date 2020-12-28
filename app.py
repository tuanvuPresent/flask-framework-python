from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from apps.common.custom_error import *

db = SQLAlchemy()
app = Flask(__name__)
CORS(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def app_config():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:1234@0.0.0.0:3306/db_mysql'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)


def app_register_errors():
    app.register_error_handler(APIException, handle_error)
    app.register_error_handler(401, error_401)
    app.register_error_handler(403, error_403)
    app.register_error_handler(404, error_404)
    app.register_error_handler(500, error_500)


def app_register_router():
    from apps.authentication.views import app_auth
    from apps.posts.views import app_post
    from apps.users.views import app_user
    app.register_blueprint(app_auth)
    app.register_blueprint(app_user)
    app.register_blueprint(app_post)


def create_app():
    app_config()
    app_register_errors()
    app_register_router()
    return app


create_app()
