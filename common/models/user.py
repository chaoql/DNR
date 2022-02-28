# coding: utf-8
from application import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False, info='昵称')
    login_name = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False, info='登陆用户名')
    login_pwd = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False, info='登陆密码')
    login_salt = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), nullable=False, info='登陆密码随机码')
    status = db.Column(db.Integer, nullable=False, info='状态 0：无效 1：有效')
    updated_time = db.Column(db.DateTime, nullable=False, info='最后更新时间')
    created_time = db.Column(db.DateTime, nullable=False, info='插入时间')
