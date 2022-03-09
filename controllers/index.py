from flask import Blueprint, request, redirect, g
from application import db
from common.models.news import News
from common.models.view import View
from common.models.user import User
from common.models.fl_data import FlDatum
from common.libs.FLHelper.Helper import ops_render, iPageNation, ops_renderJSON
from common.libs.FLHelper.UrlManager import UrlManager
from sqlalchemy.sql.expression import func
from application import app

index_page = Blueprint("index_page", __name__)


@index_page.route("/")
def index():
    page = 1
    req = request.values
    if "p" in req and req["p"]:
        page = int(req["p"])
    News_list = News.query.filter_by(hot=0).order_by(News.view_counter.desc(), News.id.desc())
    Hot_list = News.query.filter_by(hot=1).all()
    page_params = {
        "total_count": News_list.count(),
        "page_size": 10,
        "page": page,
        "url": "?"
    }
    pages = iPageNation(page_params)
    offset = (page - 1) * page_params["page_size"]
    limit = page * page_params["page_size"]
    list_news = News_list[offset:limit]
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
    model_fl = FlDatum.query.filter_by(userID=g.current_user.id, newsID=req['id']).first()
    if model_fl:
        model_fl.view_counter += 1
    else:
        model_fl = FlDatum()
        model_fl.view_counter = 1
        model_fl.userID = g.current_user.id
        model_fl.newsID = req['id']
        model_fl_news = News.query.filter_by(id=req['id']).first()
        model_fl.text = model_fl_news.text
        model_fl.genre = model_fl_news.genres
        model_fl.author = model_fl_news.authors
        model_fl.news_time = model_fl_news.date
        model_fl_user = User.query.filter_by(id=g.current_user.id).first()
        model_fl.user_gender = model_fl_user.gender
        model_fl.user_age = model_fl_user.age
    db.session.add(model_fl)
    db.session.add(model_news)
    db.session.add(model_view)
    db.session.commit()
    return ops_render("single.html", {'news': model_news,
                                      "pic_path": app.config['DOMAIN']['www'] + "static/images/news/"})


@index_page.route("/search", methods=["POST", "GET"])
def search():
    app.logger.warning("===============search===============")
    req = request.form
    app.logger.warning(req)
    app.logger.warning(request.values)
    search_str = req['search_str'] if 'search_str' in req else ""
    req = request.values
    if search_str == "":
        search_str = req['search_str'] if 'search_str' in req else ""
    model_news = News.query.filter(News.text.like("%" + search_str + "%")).all()
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
    app.logger.warning(page_params)
    pages = iPageNation(page_params)
    app.logger.warning(pages)
    offset = (page - 1) * page_params["page_size"]
    limit = page * page_params["page_size"]
    list_news = model_news[offset:limit]
    return ops_render("search.html", {'str': search_str, 'newsl': list_news, "pages": pages,
                                      "pic_path": app.config['DOMAIN']['www'] + "static/images/news/"})
