from models.db import db, User as UserModel
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_model: UserModel):
        self._user = user_model

    @property
    def id(self):
        return self._user.id

    @property
    def username(self):
        return self._user.username

    @property
    def password(self):
        return self._user.password
    
    @property
    def secret_word(self):
        return self._user.secret_answer
    
    def __repr__(self):
        return f'<User {self._user.username}>'

    def get_user_model(self):
        return self._user

    @staticmethod
    def get_by_id(user_id):
        user_model = UserModel.query.get(user_id)
        if not user_model:
            return None
        return User(user_model)

    @staticmethod
    def get_by_username(username):
        user_model = UserModel.query.filter_by(username=username).first()
        if not user_model:
            return None
        return User(user_model)

    @staticmethod
    def auth(username: str, password: str):
        user_model = UserModel.query.filter_by(username=username).first()
        if not user_model or password != user_model.password:
            return None
        return User(user_model)

    @staticmethod
    def register(username: str, password: str, secret_answer: str):
        if UserModel.query.filter_by(username=username).first():
            return None
        if secret_answer == "":
            secret_answer = None
        new_user = UserModel(
            username=username,
            password=password,
            secret_answer=secret_answer
        )

        db.session.add(new_user)
        db.session.commit()

        return User(new_user)