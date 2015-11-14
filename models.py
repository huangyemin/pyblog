from flask.ext.login import UserMixin


class User(UserMixin):
    id = '1'
    userName = 'hym'
    password = '123456'
