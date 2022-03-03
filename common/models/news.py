# coding: utf-8
from application import db


class News(db.Model):
    __tablename__ = 'news'

    NewsID = db.Column(db.Integer, primary_key=True)
    Genres = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    Title = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    Authors = db.Column(db.String(255, 'utf8_bin'))
    link = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    date = db.Column(db.String(255, 'utf8_bin'))
    text = db.Column(db.String(collation='utf8_bin'))
    photo = db.Column(db.String(255, 'utf8_bin'))
    hash = db.Column(db.String(255, 'utf8_bin'))
    vedio = db.Column(db.String(255, 'utf8_bin'))
