# coding: utf-8
from application import db


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), info='电影名称')
    classify = db.Column(db.String(255), info='类别')
    actor = db.Column(db.String(255), info='主演')
    cover_pic = db.Column(db.String(255), info='封面图')
    url = db.Column(db.String(255), info='电影详情地址')
    desc = db.Column(db.Text, info='电影描述')
    hash = db.Column(db.String(255), info='唯一值')
    pub_date = db.Column(db.String(255), info='来源网址发布日期')
    source = db.Column(db.String(255), info='来源')
    view_counter = db.Column(db.Integer, info='阅读数')
    updated_time = db.Column(db.DateTime, info='最后更新时间')
    created_time = db.Column(db.DateTime, info='插入时间')

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
