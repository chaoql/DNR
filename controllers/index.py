from flask import Flask, Blueprint, request, make_response, jsonify, render_template, redirect
from sqlalchemy import text
from application import db, app
from common.models.user import User
from common.models.movie import Movie
from common.libs.Helper import ops_render, iPageNation
from common.libs.UrlManager import UrlManager
from sqlalchemy.sql.expression import func

index_page = Blueprint("index_page", __name__)


@index_page.route("/")
def index():
    req = request.values
    order_by_f = req["order"] if ("order" in req and req["order"]) else "latest"
    page = 1
    if "p" in req and req["p"]:
        page = int(req["p"])
    query = Movie.query

    page_params = {
        "total_count": query.count(),
        "page_size": 24,
        "page": page,
        "url": "/?"
    }
    pages = iPageNation(page_params)
    # 0-23, 24-47, 48-71
    offset = (page - 1) * page_params["page_size"]
    limit = page * page_params["page_size"]
    if order_by_f == "hot":
        query = query.order_by(Movie.view_counter.desc(), Movie.id.desc())
    else:
        query = query.order_by(Movie.pub_date.desc(), Movie.id.desc())
    list_movie = query[offset:limit]
    # list_movie = query.all()
    return ops_render("index.html", {"data": list_movie, "pages": pages})  # 加载current_user对象


@index_page.route("/info")
def info():
    req = request.values
    id = int(req['id']) if ("id" in req and req["id"]) else 0
    if id < 1:
        return redirect(UrlManager.buildUrl("/"))
    info = Movie.query.filter_by(id=id).first()
    if not info:
        return redirect(UrlManager.buildUrl("/"))
    info.view_counter = info.view_counter + 1  # 浏览人数+1
    db.session.add(info)
    db.session.commit()
    recommend_list = Movie.query.order_by(func.rand()).limit(4)  # 随机推荐
    return ops_render("info.html", {'info': info, "recommend_list": recommend_list})
