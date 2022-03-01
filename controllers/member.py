from application import app, db
from flask import Blueprint, request, make_response, redirect
from common.libs.FLHelper.Helper import ops_renderJSON, ops_renderErrJSON, ops_render
from common.libs.FLHelper.UrlManager import UrlManager
from common.libs.FLHelper.DateHelper import getCurrentTime
from common.models.user import User
from common.libs.FLHelper.UserService import UserService
member_page = Blueprint("member_page", __name__)


@member_page.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        return ops_render("/member/register.html")
    req = request.values
    nick_name = req["nick_name"] if "nick_name" in req else ""
    login_name = req["login_name"] if "login_name" in req else ""
    login_pwd = req["login_pwd"] if "login_pwd" in req else ""
    login_pwd2 = req["login_pwd2"] if "login_pwd2" in req else ""
    # 因为前端可能会被穿透，所以后端要再验证一遍
    if nick_name is None or len(nick_name) < 1:
        return ops_renderErrJSON(msg="请输入正确的昵称~~~")

    if login_name is None or len(login_name) < 1:
        return ops_renderErrJSON(msg="请输入正确的用户名~~~")

    if login_pwd is None or len(login_pwd) < 1:
        return ops_renderErrJSON(msg="请输入正确的登陆密码，并且不能小于6个字符~~")

    if login_pwd != login_pwd2:
        return ops_renderErrJSON(msg="请输入正确的确认登陆密码~~")

    user_info = User.query.filter_by(login_name=login_name).first()
    if user_info:
        return ops_renderErrJSON(msg="登陆用户名已被占用，请换一个~~")

    model_user = User()
    model_user.login_name = login_name
    model_user.nickname = nick_name
    model_user.login_salt = UserService.geneSalt(8)
    model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)
    model_user.created_time = model_user.updated_time = getCurrentTime(frm="%Y-%m-%d %H:%M:%S")
    model_user.status = 1
    db.session.add(model_user)
    db.session.commit()
    response = make_response(ops_renderJSON(msg="注册成功"))
    response.set_cookie(key=app.config["AUTH_COOKIE_NAME"],
                        value="%s#%s" % (UserService.geneAuthCode(model_user), model_user.UserID),
                        max_age=60 * 60 * 24 * 120)
    return response


@member_page.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return ops_render("/member/login.html")
    req = request.values
    login_name = req["login_name"] if "login_name" in req else ""
    login_pwd = req["login_pwd"] if "login_pwd" in req else ""
    # 因为前端可能会被穿透，所以后端要再验证一遍
    if login_name is None or len(login_name) < 1:
        return ops_renderErrJSON(msg="请输入正确的用户名~~~")

    if login_pwd is None or len(login_pwd) < 1:
        return ops_renderErrJSON(msg="请输入正确的登陆密码~~")

    user_info = User.query.filter_by(login_name=login_name).first()
    if not user_info:
        return ops_renderErrJSON(msg="请输入正确的登陆用户名和密码~~")
    if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
        return ops_renderErrJSON(msg="请输入正确的登陆用户名和密码~~")
    if user_info.status != 1:
        return ops_renderErrJSON(msg="账号已被禁用，请联系管理员解决~~")
    response = make_response(ops_renderJSON(msg="登陆成功"))
    response.set_cookie(key=app.config["AUTH_COOKIE_NAME"],
                        value="%s#%s" % (UserService.geneAuthCode(user_info), user_info.UserID), max_age=60 * 60 * 24 * 120)
    return response
    # return ops_renderJSON(msg="登陆成功~~")


@member_page.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/")))
    response.delete_cookie(app.config["AUTH_COOKIE_NAME"])
    return response
