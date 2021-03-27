# TODO: Добавить проверку на уникальность пользователя и / или обработку ошибок БД

import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash
from ..model.User import User
from ..model.Todo import Todo

# Подключаемся к БД
db = sqlite3.connect(Path(__file__).parent / '..' / '..' / 'database' / 'todos_database.sqlite', check_same_thread=False)


class Storage:

    @staticmethod
    def add_user(user):
        if Storage.check_user_by_name(user.name):
            return "Пользователь с таким именем уже зарегистрирован"
        if Storage.check_user_by_email(user.email):
            return "Пользователь с данной почтой уже зарегистрирован"
        # Вместо пароля сохраняем хэш пароля
        # https://werkzeug.palletsprojects.com/en/0.16.x/utils/#werkzeug.security.generate_password_hash
        db.execute('INSERT INTO "user" (user_name, user_email, user_pass) VALUES (?, ?, ?)', (user.name, user.email, generate_password_hash(user.password)))
        db.commit()

    @staticmethod
    def check_user_by_name(name):
        return db.execute('select count(*) from "user" where "user".user_name = ?', (name,)).fetchone()[0] > 0

    @staticmethod
    def check_user_by_email(email):
        return db.execute('select count(*) from "user" where "user".user_email = ?', (email,)).fetchone()[0] > 0

    @staticmethod
    def get_user_by_name_and_password(name, password_hash):
        user_data = db.execute('select * from "user" where "user".user_name = ?', (name,)).fetchone()
        return User(*user_data) if user_data and check_password_hash(user_data[3], password_hash) else None

    @staticmethod
    def get_user_by_email_and_password(email, password_hash):
        user_data = db.execute('SELECT * FROM "user" WHERE "user".user_email = ?', (email,)).fetchone()
        # Не проверяем явно равенство паролей, а проверяем через его хэш
        # https://werkzeug.palletsprojects.com/en/0.16.x/utils/#werkzeug.security.check_password_hash
        return User(*user_data) if user_data and check_password_hash(user_data[3], password_hash) else None

    @staticmethod
    def get_user_by_id(user_id):
        user_data = db.execute('SELECT * FROM "user" WHERE "user".user_id = ?', (user_id,)).fetchone()
        return User(*user_data) if user_data else None

    @staticmethod
    def get_user_todos(user_id):
        todos = db.execute('SELECT * FROM todo WHERE todo_user_id = ?', (user_id,)).fetchall()
        return map(lambda todo: Todo(*todo), todos)

    @staticmethod
    def get_todo_by_id(todo_id):
        todo = db.execute('SELECT * FROM todo WHERE todo_id = ?', (todo_id,)).fetchone()
        return Todo(*todo)

    @staticmethod
    def add_todo(todo):
        todo_id = db.execute('INSERT INTO todo (todo_title, todo_description, todo_user_id) VALUES (?, ?, ?)',
                             (todo.name, todo.description, todo.user_id))\
            .lastrowid
        db.commit()
        todo = db.execute('SELECT * FROM todo WHERE todo_id = ?', (todo_id,)).fetchone()
        return Todo(*todo)

    @staticmethod
    def delete_todo(todo_id, user_id):
        db.execute('DELETE FROM todo WHERE todo_id = ? and todo_user_id = ?', (todo_id, user_id))
        db.commit()

    @staticmethod
    def set_todo_status(todo_id, status, user_id):
        db.execute('update todo set todo_is_done = ? where todo_id = ? and todo_user_id = ?', (status, todo_id, user_id))
        db.commit()
        todo = db.execute('SELECT * FROM todo WHERE todo_id = ? and todo_user_id = ?', (todo_id, user_id)).fetchone()
        return Todo(*todo)
