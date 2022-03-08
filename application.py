import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import flask_mysqldb
from flask_script import Manager
from flask_mail import Mail

app = Flask(__name__)
manager = Manager(app)

"""
多环境配置文件
"""
app.config.from_pyfile("config/base_setting.py")
# ops_config=local|production
os.environ["ops_config"] = "local"  # 决定导入哪一个环境配置
if "ops_config" in os.environ:
    app.config.from_pyfile("config/%s_setting.py" % (os.environ['ops_config']))

db = SQLAlchemy(app)
mail = Mail(app)
