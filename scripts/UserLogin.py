from scripts.DataBase import DataBase
from flask_login import UserMixin


class UserLogin(UserMixin):

    def create(self, user: dict) -> 'UserLogin':
        self.__user = user
        return self

    def fromDB(self, username, db: DataBase) -> 'UserLogin':
        self.__user = db.getUser(username)
        return self

    @property
    def id(self):
        return str(self.__user['id'])

    @property
    def name(self):
        return str(self.__user['name'])
