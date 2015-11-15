from flask.ext.login import UserMixin


class User(UserMixin, dict):
    def __init__(self, userDict):
        dict.__init__(self, userDict)

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def get_id(self):
        return str(self._id)
