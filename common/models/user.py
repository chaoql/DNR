# coding: utf-8
from application import db


class User(db.Model):
    __tablename__ = 'user'

    UserID = db.Column(db.Integer, primary_key=True)
    Gender = db.Column(db.Integer, nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    OccupationID = db.Column(db.Integer, nullable=False)
