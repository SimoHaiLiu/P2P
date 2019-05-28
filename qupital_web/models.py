from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime
# from flask_login import UserMixin, LoginManager
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from flask import current_app
from init import mongo


# class Role(db.Model):
#     '''
#     添加角色表
#     '''
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     def __repr__(self):
#         return '' % self.name


# class User(UserMixin):
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key = True)
#     email = db.Column(db.String(64), unique=True, index=True)
#     username = db.Column(db.String(64), unique=True, index=True)
#     password_hash = db.Column(db.String(128))
    # confirmed = db.Column(db.Boolean, default=False)

    # def __init__(self, email, username, password):
    #     self.email = email
    #     self.username = username
    #     self.password_hash = self.set_password(password)
        # self.db = mongo.db

    # def new_user(self):
    #     collection = {
    #         'email': self.email,
    #         'username': self.username,
    #         'password': self.password_hash
    #     }
    #     self.db.user.insert(collection)

    # @property
    # def password(self, password):
    #     raise AttributeError('password is not a readable attribute')
    #
    # @password.setter
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def verify_password(self, password):
    #     return check_password_hash(self.password_hash, password)
    #
    # def __repr__(self):
    #     return '' % self.username

    # def generate_confirmation_token(self, expiration=3600):
    #     '''
    #     加密确认码
    #     :param expiration:
    #     :return:
    #     '''
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'confirm': self.id})
    #
    # def confirm(self, token):
    #     '''
    #     解密确认码
    #     :param token:
    #     :return:
    #     '''
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except:
    #         return False
    #
    #     if data.get('confirm') != self.id:
    #         return False
    #
    #     self.confirmed = True
    #     db.session.add(self)
    #     return True


# @login_manager.user_loader()
# def load_user(user_id):
#     return User.query.get(int(user_id))

class User():
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.db = mongo.db

    def new_user(self):
        collection = {
            'email': self.email,
            'username': self.username,
            'password_hash': self.password_hash
        }
        self.db.users.insert(collection)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def is_active(self):
        return True

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)
