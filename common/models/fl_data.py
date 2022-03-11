# coding: utf-8
from application import db


class FlDatum(db.Model):
    __tablename__ = 'fl_data'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, nullable=False)
    newsID = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    author = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    news_time = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.String(collation='utf8_bin'), nullable=False)
    user_age = db.Column(db.Integer, nullable=False)
    user_gender = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    title = db.Column(db.String(255, 'utf8_bin'), nullable=False)
    view_counter = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
