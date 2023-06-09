import pickle
import random
from flask import Blueprint, request, redirect, g
from application import db
from common.models.news import News
from common.models.view import View
from common.models.user import User
from common.libs.FLHelper.Helper import ops_render, iPageNation, ops_renderJSON
from common.libs.FLHelper.UrlManager import UrlManager
from sqlalchemy.sql.expression import func
from application import app
from sqlalchemy import or_
from common.libs.FLHelper.Helper import load_obj
from deepLearning.predict import text_pre

index_page = Blueprint("index_page", __name__)
preView = {}

@index_page.route("/")
def index():
    page = 1
    req = request.values
    if "p" in req and req["p"]:
        page = int(req["p"])
    News_list = []
    if preView is {} or not preView:
        print("1")
        model_news = News.query.all()
        for news in model_news:
            rate = text_pre(news.title + news.text, g.current_user.age, news.view_counter, news.genres, g.current_user.id,
                            g.current_user.gender, g.current_user.occupation)
            preView[news.id] = rate
        preView_order = dict(sorted(preView.items(), key=lambda x: x[1], reverse=True))
    for newsID in preView:
        News_list.append(News.query.filter_by(id=newsID).first())
    Hot_list = News_list[0:5]
    Nomal_list = News_list[5:]
    page_params = {
        "total_count": len(Nomal_list),
        "page_size": 10,
        "page": page,
        "url": "?"
    }
    pages = iPageNation(page_params)
    offset = (page - 1) * page_params["page_size"]
    limit = page * page_params["page_size"]
    list_news = Nomal_list[offset:limit]
    return ops_render("index.html", {"newsL": list_news, "swiper": Hot_list, "pages": pages,
                                     "pic_path": app.config['DOMAIN']['www'] + "static/images/news/"})


@index_page.route("/single")
def single():
    req = request.values
    model_news = News.query.filter_by(id=req['id']).first()
    model_news.view_counter += 1
    model_view = View.query.filter_by(userID=g.current_user.id, newsID=req['id']).first()
    if model_view:
        model_view.view_counter += 1
    else:
        model_view = View()
        model_view.view_counter = 1
        model_view.userID = g.current_user.id
        model_view.newsID = req['id']
    db.session.add(model_news)
    db.session.add(model_view)
    db.session.commit()
    recommend_list = News.query.filter_by(genres=model_news.genres).order_by(func.rand()).limit(2)  # 随机推荐
    return ops_render("single.html", {'news': model_news,"recommend_list": recommend_list,
                                      "pic_path": app.config['DOMAIN']['www'] + "static/images/news/"})


@index_page.route("/search", methods=["POST", "GET"])
def search():
    req = request.form
    search_str = req['search_str'] if 'search_str' in req else ""
    req = request.values
    if search_str == "":
        search_str = req['search_str'] if 'search_str' in req else ""
    model_news = News.query.filter(or_(News.genres.like("%" + search_str + "%"),
                                       News.title.like("%" + search_str + "%"),
                                       News.date.like("%" + search_str + "%"),
                                       News.text.like("%" + search_str + "%"),
                                       News.view_counter.like(search_str))).order_by(News.date.desc(),
                                                                                     News.id.desc()).all()
    count = len(model_news)
    page = 1

    if "p" in req and req["p"]:
        page = int(req["p"])
    page_params = {
        "total_count": count,
        "page_size": 10,
        "page": page,
        "url": "search?"
    }
    pages = iPageNation(page_params)
    offset = (page - 1) * page_params["page_size"]
    limit = page * page_params["page_size"]
    list_news = model_news[offset:limit]
    return ops_render("search.html", {'str': search_str, 'newsl': list_news, "pages": pages,
                                      "pic_path": app.config['DOMAIN']['www'] + "static/images/news/"})





