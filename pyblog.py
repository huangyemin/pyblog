from flask import Flask
from flask.ext.bootstrap import Bootstrap, WebCDN
from flask.ext.login import LoginManager
from flask.ext.pymongo import PyMongo
from flask_babel import Babel


app = Flask(__name__)
bootstrap = Bootstrap(app)
mongo = PyMongo(app)
login_manager = LoginManager(app)
babel = Babel(app)

login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
app.extensions['bootstrap']['cdns']['jquery'] = WebCDN(
    '//cdn.bootcss.com/jquery/1.11.3/'
)
app.extensions['bootstrap']['cdns']['bootstrap'] = WebCDN(
    '//cdn.bootcss.com/bootstrap/3.3.5/'
)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['BABEL_DEFAULT_LOCALE'] = 'zh'

from views import *
from filters import *

if __name__ == '__main__':
    app.run(debug=True)
