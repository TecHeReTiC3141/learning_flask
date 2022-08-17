import sqlite3
from time import *


class DataBase:

    def __init__(self, db: sqlite3.Connection):
        self.__db = db
        self.__curs = db.cursor()

    def getData(self, request, data: list | tuple = (), fetch='all') -> list[dict]:
        try:
            self.__curs.execute(request, data)
            if fetch == 'all':
                res = self.__curs.fetchall()
            else:
                res = self.__curs.fetchone()
            return res
        except Exception as e:
            print(e)
        return []

    def addData(self, request, data: list | tuple = ()):
        try:
            self.__curs.execute(request, data)
            self.__db.commit()
            return 'Successfully added'
        except Exception as e:
            print(e)
            return e

    def updateData(self, request, data: list | tuple = ()):
        try:
            self.__curs.execute(request, data)
            self.__db.commit()
            return 'Successfully modified'
        except Exception as e:
            print(e)
            return e

    def getNews(self, title=None) -> list[dict]:
        if not title:
            request = f'''SELECT * FROM posts
                          ORDER BY time_posted DESC  '''
        else:
            request = f'''SELECT * FROM posts
                        WHERE title = (?)
                            ORDER BY time_posted DESC '''

        return self.getData(request, (title,) if title else (),
                            'all' if not title else 'one')

    def addNews(self, title, content, author):
        if len(title) < 4 and len(content) <= 10:
            return 'Title must be at least 4 characters long'
        time_posted = round(time())
        time_format = strftime('%d.%m.%Y at %H:%M', gmtime(time_posted))
        request = '''INSERT INTO posts (title, content, author, time_posted, time_format)
                    VALUES (?, ?, ?, ?, ?)'''
        return self.addData(request, (title, content, author, time_posted, time_format))

    def viewNews(self, title):
        request = '''UPDATE posts 
        SET views = views + 1
        WHERE title = (?)'''
        return self.updateData(request, (title,))

    def getClasses(self):
        request = '''SELECT name, descr
                                FROM Classes
                                ORDER BY name'''
        return self.getData(request)

    def getUserbyId(self, id):
        request = '''SELECT id, name, password FROM users 
                    WHERE id = (?)'''
        return self.getData(request, (id,), fetch='one')

    def getUser(self, username):
        request = '''SELECT id, name, password FROM users 
                    WHERE name = (?)'''
        return self.getData(request, (username,), fetch='one')

    def get_top_k_users(self, k=5):
        request = f'''SELECT author, SUM(views) AS views, COUNT(*) AS post
                    FROM posts JOIN users
                    ON posts.author = users.name
                    GROUP BY 1
                    ORDER BY 2 DESC
                    LIMIT {k};
                    '''
        return self.getData(request)

    def addUser(self, name, email, psw):
        prev_users = self.getData('''SELECT email FROM users
                                    WHERE email = (?)''', (email, ))
        if prev_users:
            return 'This user already exists'
        request = '''INSERT INTO users (name, email, password)
                    VALUES (?, ?, ?)'''

        return self.addData(request, (name, email, psw))
