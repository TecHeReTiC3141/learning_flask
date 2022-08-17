from scripts.DataBase import DataBase
from flask_login import UserMixin


class UserLogin(UserMixin):

    def create(self, user: dict) -> 'UserLogin':
        self.__user = user
        # print(self.__user)
        return self

    def fromDB(self, username, db: DataBase) -> 'UserLogin':
        self.__user = db.getUserbyId(username)
        print(self.__user)

        return self

    def get_id(self):
        return str(self.__user['id'])

    @property
    def name(self):
        return str(self.__user['name'])
