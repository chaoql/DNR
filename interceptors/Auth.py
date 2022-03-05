from application import app
from flask import request, g, redirect

from common.libs.FLHelper.UrlManager import UrlManager
from common.models.user import User
from common.libs.FLHelper.UserService import UserService

'''
拦截器
'''


@app.before_request
def before_request():
    app.logger.info("--------before--------")
    user_info = check_login()
    g.current_user = None
    if user_info:
        g.current_user = user_info
        return
    else:
        if request.path.endswith("/member/login") or request.path.endswith("/member/reg") \
                or request.path.endswith("/member/forgot"):
            return
        if request.path == '/' or request.path == '/member/info':
            return redirect(UrlManager.buildUrl("member/login"))
    return


@app.after_request
def after_request(response):
    app.logger.info("--------after--------")
    return response


def check_login():
    """
    判断用户是否登录
    """
    cookies = request.cookies
    cookie_name = app.config['AUTH_COOKIE_NAME']
    auth_cookie = cookies[cookie_name] if cookie_name in cookies else None
    if auth_cookie is None:
        return False

    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False

    try:
        user_info = User.query.filter_by(id=auth_info[1]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False

    return user_info
