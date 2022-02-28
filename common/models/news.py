# coding: utf-8
from application import db


class News(db.Model):
    __tablename__ = 'news'

    NewsID = db.Column(db.Integer, primary_key=True)
    Genres = db.Column(db.String(255, 'utf8_bin'))
    Title = db.Column(db.String(255, 'utf8_bin'))
    Authors = db.Column(db.String(255, 'utf8_bin'))
    link = db.Column(db.String(255, 'utf8_bin'))
    date = db.Column(db.String(255, 'utf8_bin'))
    Body = db.Column(db.String(255, 'utf8_bin'))
