import pickle

from flask import jsonify, g, render_template
import math

from application import db
from common.libs.FLHelper.DateHelper import getCurrentTime
from common.libs.FLHelper.UserService import UserService
from common.models.user import User

from sqlalchemy_utils import database_exists, create_database

from config.local_setting import SQLALCHEMY_DATABASE_URI


def db_exist():
    if database_exists(SQLALCHEMY_DATABASE_URI):
        pass
    else:
        create_database(SQLALCHEMY_DATABASE_URI)
        db.create_all()


def first_use():
    model_user = User.query.filter_by(login_name="root").first()
    if not model_user:
        model_user = User()
        model_user.nickname = "root"
        model_user.login_name = "root"
        model_user.login_salt = UserService.geneSalt(8)
        model_user.login_pwd = UserService.genePwd("123456", model_user.login_salt)
        model_user.created_time = model_user.updated_time = getCurrentTime(frm="%Y-%m-%d %H:%M:%S")
        model_user.status = 1
        model_user.power = 1
        model_user.email = "youremail@email.com"
        db.session.add(model_user)
        db.session.commit()


def load_obj(name):
    with open('./' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def save_obj(obj, name):
    with open('./' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def ops_render(template, context=None):
    if context is None:
        context = {}
    if "current_user" in g:  # current_user 变量是在拦截器中判断用户是否都登陆函数中写入全局对象g的
        context["current_user"] = g.current_user
    return render_template(template, **context)


def ops_renderJSON(code=200, msg="操作成功", data=None):
    if data is None:
        data = {}
    resp = {"code": code, "msg": msg, "data": data}
    return jsonify(resp)


def ops_renderErrJSON(msg="系统繁忙请稍后再试", data=None):
    if data is None:
        data = {}
    return ops_renderJSON(code=-1, msg=msg, data=data)


def iPageNation(params):
    """
    分页函数
    :param params: params["total_count"]=数据总条数；params["page_size"]=一页的数据量；params["page"]=当前页码
    :return:参数字典
    """
    total_count = int(params["total_count"])
    page_size = int(params["page_size"])
    page = int(params["page"])

    total_pages = math.ceil(total_count / page_size)
    total_pages = total_pages if total_pages > 0 else 1

    is_prev = 0 if page <= 1 else 1
    is_next = 0 if page >= total_pages else 1

    pages = {
        "page_size": page_size,
        "total_count": total_count,
        "total_pages": total_pages,
        "range": range(1, total_pages + 1),
        "is_next": is_next,
        "is_prev": is_prev,
        "current": page,
        "url": params["url"],
    }
    return pages


import re


##过滤HTML中的标签
# 将HTML中标签等信息去掉
# @param htmlstr HTML字符串.
def filter_tags(htmlstr):
    # 先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replaceCharEntity(s)  # 替换实体
    return s


##替换常用HTML字符实体.
# 使用正常的字符替换HTML中特殊的字符实体.
# 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
# @param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如&gt;
        key = sz.group('name')  # 去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def repalce(s, re_exp, repl_string):
    return re_exp.sub(repl_string, s)


def truncate_html(name, length=200):
    # print filter_tags(name)
    result = filter_tags(name)[0:length]
    return result
