# coding: utf-8
from application import db


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    genres = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    title = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    authors = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    link = db.Column(db.String(collation='utf8_bin'), nullable=False)
    date = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    text = db.Column(db.String(collation='utf8_bin'), nullable=False)
    photo = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    hash = db.Column(db.String(255, 'utf8_bin'), primary_key=True, nullable=False)
    view_counter = db.Column(db.Integer, nullable=False)
