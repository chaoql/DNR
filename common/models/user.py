# coding: utf-8
from application import db


class User(db.Model):
    __tablename__ = 'user'

    UserID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Gender = db.Column(db.Integer)
    Age = db.Column(db.Integer)
    OccupationID = db.Column(db.Integer)
    nickname = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    login_name = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    login_pwd = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    login_salt = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    updated_time = db.Column(db.DateTime, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False)
