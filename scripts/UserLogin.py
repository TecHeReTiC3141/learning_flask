from scripts.DataBase import DataBase


class UserLogin:

    def create(self, user: dict) -> 'UserLogin':
        self.__user = user
        return self

    def fromDB(self, username, db: DataBase):
        self.__user = db.getUser(username)
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user['id'])
