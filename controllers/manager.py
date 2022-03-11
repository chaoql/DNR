from flask import Blueprint, request, redirect, g
from application import db, app
from common.libs.FLHelper.Helper import iPageNation, ops_render
from common.libs.FLHelper.UrlManager import UrlManager
from common.models.fl_data import FlDatum
from common.models.user import User
from common.models.view import View
from sqlalchemy import or_
manager_page = Blueprint("manager_page", __name__)


@manager_page.route("/")
def showUser():
    req = request.values
    page = 1
    if "p" in req and req["p"]:
        page = int(req["p"])
    query = User.query.filter_by(power=0).all()
    page_params = {
        "total_count": len(query),
        "page_size": 24,
        "page": page,
        "url": "manager?"
    }
    pages = iPageNation(page_params)
    # 0-23, 24-47, 48-71
    offset = (page - 1) * page_params["page_size"]
    limit = page * page_params["page_size"]
    query = User.query.filter_by(power=0).order_by(User.created_time.desc(), User.id.desc())
    userl = query[offset:limit]
    return ops_render("manager/userManager.html", {"data": userl, "pages": pages})  # 加载current_user对象


@manager_page.route("/delete")
def delete():
    req = request.values
    uid = int(req["id"]) if "id" in req and req["id"] else -1
    app.logger.warning(uid)
    app.logger.warning("======================================")
    model_user = User.query.filter_by(id=uid).first()
    if model_user:
        db.session.delete(model_user)
        model_view = View.query.filter_by(userID=uid).all()
        if model_view:
            for view in model_view:
                db.session.delete(view)
        model_fl = FlDatum.query.filter_by(userID=uid).all()
        if model_fl:
            for fl in model_fl:
                db.session.delete(fl)
    db.session.commit()
    return redirect(UrlManager.buildUrl("manager/"))


@manager_page.route("/search", methods=["POST", "GET"])
def search():
    req = request.form
    search_str = req['search_str'] if 'search_str' in req else ""
    req = request.values
    if search_str == "":
        search_str = req['search_str'] if 'search_str' in req else ""
    model_user = User.query.filter(or_(User.gender.like("%" + search_str + "%"),
                                   User.login_name.like("%" + search_str + "%"),
                                   User.nickname.like("%" + search_str + "%"),
                                   User.age.like("%" + search_str + "%"),
                                   User.email.like("%" + search_str + "%"))).filter_by(power=0).all()
    count = len(model_user)
    page = 1

    if "p" in req and req["p"]:
        page = int(req["p"])
    page_params = {
        "total_count": count,
        "page_size": 24,
        "page": page,
        "url": "manager/search?"
    }
    pages = iPageNation(page_params)
    offset = (page - 1) * page_params["page_size"]
    limit = page * page_params["page_size"]
    userl = model_user[offset:limit]
    return ops_render("manager/search.html", {"data": userl, "pages": pages})


@manager_page.route("/modify")
def modify():
    pass


@manager_page.route("/add")
def add():
    pass