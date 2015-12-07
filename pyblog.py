from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.pymongo import PyMongo
from flask_babel import Babel
from flask_moment import Moment

from config import config

bootstrap = Bootstrap()
mongo = PyMongo()
login_manager = LoginManager()
babel = Babel()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)
    moment.init_app(app)

    config[config_name].init_app(app)

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'login'

    return app
