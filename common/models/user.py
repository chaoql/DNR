# coding: utf-8
from application import db


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
