from .model import *

class UserCollection:
    def query(self):
        return Session.query(User)

    def add(self, username):
        user = User(username=username)
        Session.add(user)
        return user
