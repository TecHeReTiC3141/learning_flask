from scripts.DataBase import DataBase
from flask_login import UserMixin
from app import app
from flask import url_for


class UserLogin(UserMixin):
    possible_exts = ['png']

    def create(self, user: dict) -> 'UserLogin':
        self.__user = user
        return self

    def fromDB(self, username, db: DataBase) -> 'UserLogin':
        self.__user = db.getUserbyId(username)
        return self

    def get_id(self):
        return str(self.__user['id'])

    @property
    def name(self):
        return self.__user['name'] if self.__user else 'No name'

    @property
    def email(self):
        return self.__user['email'] if self.__user else 'No email'

    @property
    def avatar(self):
        if self.__user['avatar']:
            return self.__user['avatar']
        try:
            with open(app.root_path + url_for('static', filename='images/default_avatar.png'),
                      'rb') as f:
                img = f.read()
            return img
        except Exception as e:
            print('Default not found', e)

    def checkExt(self, file_name: str):
        ext = file_name.rsplit('.', 1)[1]
        return ext.lower() in self.possible_exts
