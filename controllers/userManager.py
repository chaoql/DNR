from flask import Blueprint, request, redirect, g
from application import db, app
from common.libs.FLHelper.DateHelper import getCurrentTime
from common.libs.FLHelper.Helper import iPageNation, ops_render, ops_renderErrJSON, ops_renderJSON
from common.libs.FLHelper.UrlManager import UrlManager
from common.libs.FLHelper.UserService import UserService
from common.models.user import User
from common.models.view import View
from sqlalchemy import or_

userManager_page = Blueprint("userManager_page", __name__)


@userManager_page.route("/")
def showUser():
    req = request.values
    page = 1
    if "p" in req and req["p"]:
        page = int(req["p"])
    query = User.query.filter_by(power=0).order_by(User.created_time.desc(), User.id.desc()).all()
    page_params = {
        "total_count": len(query),
        "page_size": 24,
        "page": page,
        "url": "userManager?"
    }
    pages = iPageNation(page_params)
    # 0-23, 24-47, 48-71
    offset = (page - 1) * page_params["page_size"]
    limit = page * page_params["page_size"]
    # query = User.query.filter_by(power=0).order_by(User.created_time.desc(), User.id.desc())
    userl = query[offset:limit]
    return ops_render("userManager/userManager.html", {"data": userl, "pages": pages})


@userManager_page.route("/delete")
def delete():
    req = request.values
    uid = int(req["id"]) if "id" in req and req["id"] else -1
    model_user = User.query.filter_by(id=uid).first()
    if model_user:
        db.session.delete(model_user)
        model_view = View.query.filter_by(userID=uid).all()
        if model_view:
            for view in model_view:
                db.session.delete(view)
    db.session.commit()
    return redirect(UrlManager.buildUrl("userManager/"))


@userManager_page.route("/search", methods=["POST", "GET"])
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
        "url": "userManager/search?"
    }
    pages = iPageNation(page_params)
    offset = (page - 1) * page_params["page_size"]
    limit = page * page_params["page_size"]
    userl = model_user[offset:limit]
    return ops_render("userManager/search.html", {"str": search_str, "data": userl, "pages": pages})


@userManager_page.route("/modify", methods=["POST", "GET"])
def modify():
    if request.method == "GET":
        req = request.values
        uid = int(req["id"]) if "id" in req and req["id"] else -1
        page = 1
        if "p" in req and req["p"]:
            page = int(req["p"])
        query = User.query.filter_by(power=0).order_by(User.created_time.desc(), User.id.desc()).all()
        page_params = {
            "total_count": len(query),
            "page_size": 24,
            "page": page,
            "url": "userManager/modify?"
        }
        pages = iPageNation(page_params)
        offset = (page - 1) * page_params["page_size"]
        limit = page * page_params["page_size"]
        userl = query[offset:limit]
        return ops_render("userManager/modify.html", {"data": userl, "spid": uid, "pages": pages})
    req = request.values
    nick_name = req["nick_name"] if "nick_name" in req else ""
    login_name = req["login_name"] if "login_name" in req else ""
    gender = req["gender"] if "gender" in req else ""
    age = int(req["age"]) if "age" in req else -1
    use = req["use"] if "use" in req else ""
    occupation = req["occupation"] if "occupation" in req else ""
    occ_list = ["Student", "Teacher", "Engineer", "Researcher", "Doctor", "Policeman", "Others"]
    model_user = User.query.filter_by(login_name=login_name).first()
    if nick_name is None or len(nick_name) < 1:
        return ops_renderErrJSON(msg="请输入正确的昵称~~~")

    if gender == "":
        gender = model_user.gender

    if gender is None or len(gender) < 1 or (gender != "Female" and gender != "Male"):
        return ops_renderErrJSON(msg="请选择正确的性别~~~")
    if use == "":
        if model_user.status == 1:
            use = "using"
        else:
            use = "not using"

    if use is None or len(use) < 1 or (use != "using" and use != "not using"):
        return ops_renderErrJSON(msg="请选择正确的用户状态~~~")

    if age > 100 or age < 0:
        return ops_renderErrJSON(msg="请输入正确的年龄~~~")

    if occupation == "":
        occupation = model_user.occupation

    if occupation is None or len(occupation) < 1 or occupation not in occ_list:
        return ops_renderErrJSON(msg="请选择正确的职业~~~")
    if nick_name == model_user.nickname and gender == model_user.gender \
            and (True if (
            (use == "using" and model_user.status == 1) or (
            use == "not using" and model_user.status == 0)) else False) and age == model_user.age \
            and occupation == model_user.occupation:
        return ops_renderJSON(msg="信息未变动~~")
    else:
        model_user.nickname = nick_name
        model_user.gender = gender
        model_user.age = age
        model_user.occupation = occupation
        model_user.status = 1 if use == "using" else 0
        db.session.add(model_user)
        db.session.commit()
        return ops_renderJSON(msg="信息修改成功~~")


@userManager_page.route("/add", methods=["POST", "GET"])
def add():
    if request.method == 'GET':
        req = request.values
        page = 1
        if "p" in req and req["p"]:
            page = int(req["p"])
        query = User.query.filter_by(power=0).order_by(User.created_time.desc(), User.id.desc()).all()
        page_params = {
            "total_count": len(query),
            "page_size": 24,
            "page": page,
            "url": "userManager/add?"
        }
        pages = iPageNation(page_params)
        offset = (page - 1) * page_params["page_size"]
        limit = page * page_params["page_size"]
        userl = query[offset:limit]
        return ops_render("userManager/adduser.html", {"data": userl, "pages": pages})
    req = request.values
    nick_name = req["nick_name"] if "nick_name" in req else ""
    login_name = req["login_name"] if "login_name" in req else ""
    gender = req["gender"] if "gender" in req else ""
    age = int(req["age"]) if "age" in req else -1
    use = req["use"] if "use" in req else ""
    occupation = req["occupation"] if "occupation" in req else ""
    email = req["email"] if "email" in req else ""
    login_pwd = "666666"  # 默认密码为666666
    occ_list = ["Student", "Teacher", "Engineer", "Researcher", "Doctor", "Policeman", "Others"]
    model_user = User.query.filter_by(login_name=login_name).first()
    if model_user:
        return ops_renderErrJSON(msg="用户名已存在~~~")

    if nick_name is None or len(nick_name) < 1:
        return ops_renderErrJSON(msg="请输入正确的昵称~~~")

    if login_name is None or len(login_name) < 1:
        return ops_renderErrJSON(msg="请输入正确的用户名~~~")

    if gender is None or len(gender) < 1 or (gender != "Female" and gender != "Male"):
        return ops_renderErrJSON(msg="请选择正确的性别~~~")

    if use is None or len(use) < 1 or (use != "using" and use != "not using"):
        return ops_renderErrJSON(msg="请选择正确的用户状态~~~")

    if age > 100 or age < 0:
        return ops_renderErrJSON(msg="请输入正确的年龄~~~")

    if occupation is None or len(occupation) < 1 or occupation not in occ_list:
        return ops_renderErrJSON(msg="请选择正确的职业~~~")

    if email is None or len(email) < 1:
        return ops_renderErrJSON(msg="请输入正确的邮箱~~~")
    model_user = User()
    model_user.nickname = nick_name
    model_user.gender = gender
    model_user.login_name = login_name
    model_user.age = age
    model_user.occupation = occupation
    model_user.login_salt = UserService.geneSalt(8)
    model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)
    model_user.created_time = model_user.updated_time = getCurrentTime(frm="%Y-%m-%d %H:%M:%S")
    model_user.status = 1 if use == "using" else 0
    model_user.power = 0
    model_user.email = email
    db.session.add(model_user)
    db.session.commit()
    return ops_renderJSON(msg="用户添加成功~~~")
