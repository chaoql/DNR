from application import app, db
from flask import Blueprint, request, make_response, redirect, g
from common.libs.FLHelper.Helper import ops_renderJSON, ops_renderErrJSON, ops_render
from common.libs.FLHelper.UrlManager import UrlManager
from common.libs.FLHelper.DateHelper import getCurrentTime
from common.models.user import User
from common.libs.FLHelper.UserService import UserService
from common.libs.FLHelper.MailService import send_reset_pwd_email

member_page = Blueprint("member_page", __name__)


@member_page.route("/reg", methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        return ops_render("/member/register.html")
    req = request.values
    nick_name = req["nick_name"] if "nick_name" in req else ""
    login_name = req["login_name"] if "login_name" in req else ""
    email = req["email"] if "email" in req else ""
    login_pwd = req["login_pwd"] if "login_pwd" in req else ""
    login_pwd2 = req["login_pwd2"] if "login_pwd2" in req else ""
    # 因为前端可能会被穿透，所以后端要再验证一遍
    if nick_name is None or len(nick_name) < 1:
        return ops_renderErrJSON(msg="请输入正确的昵称~~~")

    if login_name is None or len(login_name) < 1:
        return ops_renderErrJSON(msg="请输入正确的用户名~~~")

    if email is None or len(email) < 1:
        return ops_renderErrJSON(msg="请输入正确的邮箱~~~")

    if login_pwd is None or len(login_pwd) < 1:
        return ops_renderErrJSON(msg="请输入正确的登陆密码，并且不能小于6个字符~~")

    if login_pwd != login_pwd2:
        return ops_renderErrJSON(msg="请输入正确的确认登陆密码~~")

    user_info = User.query.filter_by(login_name=login_name).first()
    if user_info:
        return ops_renderErrJSON(msg="登陆用户名已被占用，请换一个~~")

    global reg_model_user
    reg_model_user = User()
    reg_model_user.login_name = login_name
    reg_model_user.nickname = nick_name
    reg_model_user.email = email
    reg_model_user.login_salt = UserService.geneSalt(8)
    reg_model_user.login_pwd = UserService.genePwd(login_pwd, reg_model_user.login_salt)
    reg_model_user.created_time = reg_model_user.updated_time = getCurrentTime(frm="%Y-%m-%d %H:%M:%S")
    reg_model_user.status = 1
    # db.session.add(model_user)
    # db.session.commit()
    response = make_response(ops_renderJSON(msg="注册成功(1/2),请继续完善信息~~~"))
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
                        value="%s#%s" % (UserService.geneAuthCode(user_info), user_info.id),
                        max_age=60 * 60 * 24 * 120)
    return response


@member_page.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/")))
    response.delete_cookie(app.config["AUTH_COOKIE_NAME"])
    return response


@member_page.route("/forgot", methods=["POST", "GET"])
def forgot():
    if request.method == "GET":
        return ops_render("/member/forgot.html")
    req = request.values
    email = req["email"] if "email" in req else ""
    if email is None or len(email) < 1:
        return ops_renderErrJSON(msg="请输入正确的邮箱~~")
    model_user = User.query.filter_by(email=email).first()
    emails = [email]
    if model_user:
        send_reset_pwd_email(model_user, re=emails)
    else:
        return ops_renderErrJSON(msg="请输入正确的邮箱~~")
    return ops_renderJSON(msg="请注意查收邮件并操作~~")


@member_page.route("/f_reset", methods=["POST", "GET"])
def f_reset():
    if request.method == "GET":
        return ops_render("/member/f_reset.html")
    req = request.values
    model_user = User.verify_token(req["token"])
    new_pwd = req["new_pwd"] if "new_pwd" in req else ""
    new_pwd2 = req["new_pwd2"] if "new_pwd2" in req else ""

    app.logger.warning("===============f_reset==============")
    app.logger.warning(req)
    app.logger.warning(model_user)
    app.logger.warning("------------------------------------")
    # 因为前端可能会被穿透，所以后端要再验证一遍
    if new_pwd is None or len(new_pwd) < 6:
        return ops_renderErrJSON(msg="请输入正确的新登陆密码，并且不能小于6个字符~~")
    if new_pwd2 is None or len(new_pwd2) < 6 or new_pwd != new_pwd2:
        return ops_renderErrJSON(msg="请输入正确的确认新登陆密码~~")
    if model_user:
        model_user.login_pwd = UserService.genePwd(new_pwd, model_user.login_salt)
        db.session.add(model_user)
        db.session.commit()
        return ops_renderJSON(msg="密码重置成功~~")
    else:
        return ops_renderErrJSON(msg="密码重置失败~~")


@member_page.route("/reset", methods=["POST", "GET"])
def reset():
    if request.method == "GET":
        return ops_render("/member/reset.html")
    req = request.values
    old_pwd = req["old_pwd"] if "old_pwd" in req else ""
    new_pwd = req["new_pwd"] if "new_pwd" in req else ""
    new_pwd2 = req["new_pwd2"] if "new_pwd2" in req else ""
    # 因为前端可能会被穿透，所以后端要再验证一遍
    if old_pwd is None or len(old_pwd) < 6:
        return ops_renderErrJSON(msg="请输入正确的旧登陆密码~~")
    if new_pwd is None or len(new_pwd) < 6:
        return ops_renderErrJSON(msg="请输入正确的新登陆密码，并且不能小于6个字符~~")
    if new_pwd2 is None or len(new_pwd2) < 6 or new_pwd != new_pwd2:
        return ops_renderErrJSON(msg="请输入正确的确认新登陆密码~~")
    tmp_pwd = UserService.genePwd(old_pwd, g.current_user.login_salt)
    model_user = User.query.filter_by(login_pwd=tmp_pwd).first()
    if model_user:
        model_user.login_pwd = UserService.genePwd(new_pwd, g.current_user.login_salt)
        db.session.add(model_user)
        db.session.commit()
        return ops_renderJSON(msg="密码修改成功~~")
    else:
        return ops_renderErrJSON(msg="密码输入错误~~")


@member_page.route("/info", methods=["POST", "GET"])
def info():
    if request.method == "GET":
        return ops_render("/member/info.html")
    req = request.values
    gender = req["gender"] if "gender" in req else ""
    age = int(req["age"]) if "age" in req else -1
    occupation = req["occupation"] if "occupation" in req else ""
    occ_list = ["Student", "Teacher", "Engineer", "Researcher", "Doctor", "Policeman", "Others"]
    # 因为前端可能会被穿透，所以后端要再验证一遍
    if gender is None or len(gender) < 1 or (gender != "Female" and gender != "Male"):
        return ops_renderErrJSON(msg="请输入正确的性别~~~")

    if age > 100 or age < 0:
        return ops_renderErrJSON(msg="请输入正确的年龄~~~")

    if occupation is None or len(occupation) < 1 or occupation not in occ_list:
        return ops_renderErrJSON(msg="请输入正确的职业~~~")

    # model_user = User.query.filter_by(login_name=g.current_user.login_name).first()
    reg_model_user.gender = gender
    reg_model_user.age = age
    reg_model_user.occupation = occupation
    reg_model_user.power = 0  # 0为普通用户，1为管理员
    db.session.add(reg_model_user)
    db.session.commit()
    response = make_response(ops_renderJSON(msg="注册成功(2/2)~~"))
    response.set_cookie(key=app.config["AUTH_COOKIE_NAME"],
                        value="%s#%s" % (UserService.geneAuthCode(reg_model_user), reg_model_user.id),
                        max_age=60 * 60 * 24 * 120)
    return response


@member_page.route("/profile")
def profile():
    return ops_render("member/profile.html", {'userl': g.current_user})


@member_page.route("/commit_pro", methods=["POST", "GET"])
def commit_pro():
    req = request.values
    nick_name = req["nick_name"] if "nick_name" in req else ""
    login_name = req["login_name"] if "login_name" in req else ""
    gender = req["gender"] if "gender" in req else ""
    age = int(req["age"]) if "age" in req else -1
    occupation = req["occupation"] if "occupation" in req else ""
    occ_list = ["Student", "Teacher", "Engineer", "Researcher", "Doctor", "Policeman", "Others"]
    if nick_name is None or len(nick_name) < 1:
        return ops_renderErrJSON(msg="请输入正确的昵称~~~")

    if login_name is None or len(login_name) < 1:
        return ops_renderErrJSON(msg="请输入正确的用户名~~~")

    if gender is None or len(gender) < 1 or (gender != "Female" and gender != "Male"):
        return ops_renderErrJSON(msg="请输入正确的性别~~~")

    if age > 100 or age < 0:
        return ops_renderErrJSON(msg="请输入正确的年龄~~~")

    if occupation is None or len(occupation) < 1 or occupation not in occ_list:
        return ops_renderErrJSON(msg="请输入正确的职业~~~")
    if nick_name == g.current_user.nickname and login_name == g.current_user.login_name and gender == g.current_user.gender \
            and age == g.current_user.age and occupation == g.current_user.occupation:
        return ops_renderJSON(msg="信息未变动~~")
    else:
        model_user = User.query.filter_by(id=g.current_user.id).first()
        model_user.nickname = nick_name
        model_user.login_name = login_name
        model_user.gender = gender
        model_user.age = age
        model_user.occupation = occupation
        db.session.add(model_user)
        db.session.commit()
        return ops_renderJSON(msg="信息修改成功~~")
