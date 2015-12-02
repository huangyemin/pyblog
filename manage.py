#!/usr/bin/env python
import os

from flask.ext.script import Manager, Shell

from pyblog import create_app

config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)
from views import *

manager = Manager(app)


def make_shell_context():
    return dict(app=app)


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.option('-u', '--userName', dest='userName', default=app.config['DEFAULT_USER'])
@manager.option('-p', '--password', dest='password', default='123456')
@manager.option('-n', '--nickName', dest='nickName', default=None)
def create_user(userName, password, nickName):
    mongo.db.users.remove({"userName": userName})
    if not nickName:
        nickName = userName
    mongo.db.users.insert({'userName': userName, 'password': generate_password_hash(password), 'nickName': nickName})


if __name__ == '__main__':
    manager.run()
