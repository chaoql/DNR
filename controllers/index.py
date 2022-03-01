from flask import Blueprint, request, redirect
from application import db
from common.models.news import News
from common.libs.FLHelper.Helper import ops_render, iPageNation
from common.libs.FLHelper.UrlManager import UrlManager
from sqlalchemy.sql.expression import func

index_page = Blueprint("index_page", __name__)


@index_page.route("/")
def index():
    return ops_render("index.html")  # 加载current_user对象
