# coding: utf-8
from application import db


class Rating(db.Model):
    __tablename__ = 'rating'

    RatingID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, nullable=False)
    NewsID = db.Column(db.Integer, nullable=False)
    Rating = db.Column(db.Integer, nullable=False)
