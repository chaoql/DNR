from flask import jsonify, g, render_template
import math


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
