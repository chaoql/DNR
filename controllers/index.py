from flask import Blueprint, request, redirect
from application import db
from common.models.news import News
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
    return ops_render("single.html",
                      {'news': model_news, "pic_path": app.config['DOMAIN']['www'] + "static/images/news/"})


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
