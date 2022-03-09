# coding: utf-8
from application import db


class View(db.Model):
    __tablename__ = 'view'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    userID = db.Column(db.Integer, nullable=False)
    newsID = db.Column(db.Integer, nullable=False)
    view_counter = db.Column(db.Integer, nullable=False)
