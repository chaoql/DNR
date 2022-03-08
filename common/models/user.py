# coding: utf-8
from time import time
import jwt

from application import db, app


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(255, 'utf8_bin'))
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(255, 'utf8_bin'))
    nickname = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    login_name = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    login_pwd = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    login_salt = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255, 'utf8_bin'), nullable=False)

    def get_token(self, expires_in=600):
        context = jwt.encode({'reset_pwd': self.id, 'exp': time()+expires_in}, app.config['SECRET_KEY'],
                             algorithm='HS256')
        return context

    @staticmethod
    def verify_token(token):
        tmp_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_pwd']
        app.logger.warning("===============user.py===============")
        app.logger.warning(tmp_id)
        app.logger.warning("-------------------------------------")
        return User.query.filter_by(id=tmp_id).first()
