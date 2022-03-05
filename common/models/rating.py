# coding: utf-8
from application import db


class Rating(db.Model):
    __tablename__ = 'rating'

    ratingID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, nullable=False)
    newsID = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
