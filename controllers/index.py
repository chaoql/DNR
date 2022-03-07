from flask import Blueprint, request, redirect
from application import db
from common.models.news import News
from common.libs.FLHelper.Helper import ops_render, iPageNation
from common.libs.FLHelper.UrlManager import UrlManager
from sqlalchemy.sql.expression import func
from application import app

index_page = Blueprint("index_page", __name__)


@index_page.route("/")
def index():
    News_list = News.query.order_by(News.view_counter.desc(), News.id.desc())
    return ops_render("index.html", {"newsL": News_list[5:10], "swiper": News_list[0:5],
                                     "pic_path": app.config['DOMAIN']['www'] + "static/images/news/"})


@index_page.route("/single")
def sigal():
    return ops_render("single.html")
