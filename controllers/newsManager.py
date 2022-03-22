import hashlib
import re
from flask import Blueprint, request, redirect, g
from application import db, app
from common.libs.FLHelper.DateHelper import getCurrentTime
from common.libs.FLHelper.Helper import iPageNation, ops_render, ops_renderErrJSON, ops_renderJSON
from common.libs.FLHelper.UrlManager import UrlManager
from common.libs.FLHelper.UserService import UserService
from common.models.news import News
from common.models.user import User
from common.models.view import View
from sqlalchemy import or_

newsManager_page = Blueprint("newsManager_page", __name__)
Tmodel_news = News()

@newsManager_page.route("/")
def showUser():
    req = request.values
    page = 1
    if "p" in req and req["p"]:
        page = int(req["p"])
    query = News.query.order_by(News.date.desc(), News.id.desc()).all()
    page_params = {
        "total_count": len(query),
        "page_size": 24,
        "page": page,
        "url": "newsManager?"
    }
    pages = iPageNation(page_params)
    # 0-23, 24-47, 48-71
    offset = (page - 1) * page_params["page_size"]
    limit = page * page_params["page_size"]
    # query = User.query.filter_by(power=0).order_by(User.created_time.desc(), User.id.desc())
    newsl = query[offset:limit]
    return ops_render("newsManager/newsManager.html", {"data": newsl, "pages": pages})


@newsManager_page.route("/delete")
def delete():
    req = request.values
    nid = int(req["id"]) if "id" in req and req["id"] else -1
    model_news = News.query.filter_by(id=nid).first()
    if model_news:
        db.session.delete(model_news)
        model_view = View.query.filter_by(newsID=nid).all()
        if model_view:
            for view in model_view:
                db.session.delete(view)
    db.session.commit()
    return redirect(UrlManager.buildUrl("newsManager/"))


@newsManager_page.route("/search", methods=["POST", "GET"])
def search():
    req = request.form
    search_str = req['search_str'] if 'search_str' in req else ""
    req = request.values
    if search_str == "":
        search_str = req['search_str'] if 'search_str' in req else ""
    model_news = News.query.filter(or_(News.genres.like("%" + search_str + "%"),
                                       News.title.like("%" + search_str + "%"),
                                       News.date.like("%" + search_str + "%"),
                                       News.text.like("%" + search_str + "%"),
                                       News.view_counter.like(search_str))).order_by(News.date.desc(),
                                                                                     News.id.desc()).all()
    count = len(model_news)
    page = 1

    if "p" in req and req["p"]:
        page = int(req["p"])
    page_params = {
        "total_count": count,
        "page_size": 24,
        "page": page,
        "url": "newsManager/search?"
    }
    pages = iPageNation(page_params)
    offset = (page - 1) * page_params["page_size"]
    limit = page * page_params["page_size"]
    newsl = model_news[offset:limit]
    return ops_render("newsManager/search.html", {'str': search_str, "data": newsl, "pages": pages})


@newsManager_page.route("/modify", methods=["POST", "GET"])
def modify():
    if request.method == "GET":
        req = request.values
        nid = int(req["id"]) if "id" in req and req["id"] else -1
        page = 1
        if "p" in req and req["p"]:
            page = int(req["p"])
        query = News.query.order_by(News.date.desc(), News.id.desc()).all()
        page_params = {
            "total_count": len(query),
            "page_size": 24,
            "page": page,
            "url": "newsManager/modify?"
        }
        pages = iPageNation(page_params)
        # 0-23, 24-47, 48-71
        offset = (page - 1) * page_params["page_size"]
        limit = page * page_params["page_size"]
        # query = User.query.filter_by(power=0).order_by(User.created_time.desc(), User.id.desc())
        newsl = query[offset:limit]
        app.logger.warning("*********************newsText get***********************")
        return ops_render("newsManager/modify.html", {"data": newsl, "spid": nid, "pages": pages})
    req = request.values
    id = req["id"] if "id" in req else ""
    title = req["title"] if "title" in req else ""
    genre = req["genre"] if "genre" in req else ""
    authors = req["authors"] if "authors" in req else ""
    date = req["date"] if "date" in req else ""
    view = req["view"] if "view" in req else ""
    genre_list = ["antip", "ent", "milite", "world", "tech", "finance"]
    global Tmodel_news
    Tmodel_news = News.query.filter_by(id=id).first()
    if title is None or len(title) < 1:
        return ops_renderErrJSON(msg="请输入正确的新闻题目~~~")

    if genre == "":
        genre = Tmodel_news.genres

    if genre is None or len(genre) < 1 or genre not in genre_list:
        return ops_renderErrJSON(msg="请选择正确的新闻类别~~~")

    if authors is None or len(authors) < 1:
        return ops_renderErrJSON(msg="请输入正确的新闻作者~~~")

    # 匹配日期格式
    ret = re.match("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", date)
    if ret == None:
        return ops_renderErrJSON(msg="请输入正确的新闻发布时间，如：2022-03-18 17:12:00~~~")

    if str.isdigit(view) == False or str == "":
        return ops_renderErrJSON(msg="请输入正确的新闻阅读数~~~")

    app.logger.warning("*********************modify post***********************")
    app.logger.warning(title)
    app.logger.warning(genre)
    app.logger.warning(authors)
    app.logger.warning(date)
    app.logger.warning(view)
    app.logger.warning(Tmodel_news.hash)
    if title == Tmodel_news.title and genre == Tmodel_news.genres and int(view) == Tmodel_news.view_counter \
            and authors == Tmodel_news.authors and date == Tmodel_news.date:
        return ops_renderJSON(msg="信息未变动~~")
    else:
        Tmodel_news.title = title
        Tmodel_news.genres = genre
        Tmodel_news.view_counter = int(view)
        Tmodel_news.authors = authors
        Tmodel_news.date = date
        # db.session.add(model_news)
        # db.session.commit()
        return ops_renderJSON(msg="信息修改成功~~")


@newsManager_page.route("/add", methods=["POST", "GET"])
def add():
    if request.method == 'GET':
        req = request.values
        page = 1
        if "p" in req and req["p"]:
            page = int(req["p"])
        query = News.query.order_by(News.date.desc(), News.id.desc()).all()
        page_params = {
            "total_count": len(query),
            "page_size": 24,
            "page": page,
            "url": "newsManager/add?"
        }
        pages = iPageNation(page_params)
        # 0-23, 24-47, 48-71
        offset = (page - 1) * page_params["page_size"]
        limit = page * page_params["page_size"]
        newsl = query[offset:limit]
        return ops_render("newsManager/addnews.html",
                          {"data": newsl, "pages": pages, "date": getCurrentTime("%Y-%m-%d %H:%M:%S")})
    req = request.values
    title = req["title"] if "title" in req else ""
    genre = req["genre"] if "genre" in req else ""
    authors = req["authors"] if "authors" in req else ""
    date = req["date"] if "date" in req else ""
    view = req["view"] if "view" in req else ""
    link = req["link"] if "link" in req else ""
    genre_list = ["antip", "ent", "milite", "world", "tech", "finance"]
    app.logger.warning(title)
    app.logger.warning(genre)
    app.logger.warning(authors)
    app.logger.warning(date)
    app.logger.warning(view)
    if title is None or len(title) < 1:
        return ops_renderErrJSON(msg="请输入正确的新闻题目~~~")

    if genre is None or len(genre) < 1 or genre not in genre_list:
        return ops_renderErrJSON(msg="请选择正确的新闻类别~~~")

    if authors is None or len(authors) < 1:
        return ops_renderErrJSON(msg="请输入正确的新闻作者~~~")

    # 匹配网站url格式
    ret = re.match("(http|https):\/\/([\w-]+\.)+[\w-]+(\/[\w.-\/?%&=]*)?", link)
    if ret is None:
        return ops_renderErrJSON(msg="请输入正确的来源网址~~~")

    # 匹配日期格式
    ret = re.match("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", date)
    if ret is None:
        return ops_renderErrJSON(msg="请输入正确的新闻发布时间，如：2022-03-18 17:12:00~~~")

    if str.isdigit(view) == False or str == "":
        return ops_renderErrJSON(msg="请输入正确的新闻阅读数~~~")

    # model_news = News()
    Tmodel_news.title = title
    Tmodel_news.link = link
    Tmodel_news.genres = genre
    Tmodel_news.view_counter = int(view)
    Tmodel_news.authors = authors
    Tmodel_news.date = date
    Tmodel_news.hash = hashlib.md5(link.encode("utf-8")).hexdigest()
    # db.session.add(model_news)
    # db.session.commit()
    return ops_renderJSON(msg="新闻添加成功(1/2)~~~")


@newsManager_page.route("/newstext", methods=["POST", "GET"])
def newstext():
    if request.method == "GET":
        req = request.values
        id = req["id"] if "id" in req else ""
        if id:
            text = News.query.filter_by(id=id).first().text
        else:
            text = ""
        return ops_render("newsText.html", {"data": text})
    else:
        f = request.form
        text = f["text"] if "text" in f else ""
        photo = request.files.get("photo")

        if text is None or len(text) < 1:
            return ops_renderErrJSON(msg="新闻文本为空")

        if photo is None and Tmodel_news.photo is None:
            return ops_renderErrJSON(msg="图片链接为空")

        if photo is not None:
            end_name = photo.filename.rsplit('.')[-1]
            if end_name not in ['JPG', 'jpg', 'png', 'gif', 'jpeg', 'bmp']:
                return ops_renderErrJSON("图片格式错误，仅接受jpg, png, gif, jpeg, bmp格式的图片！")
            photo.save("E:/毕业设计/dnr-bisher/static/images/news/" + Tmodel_news.hash + ".jpg")
            Tmodel_news.photo = photo

        Tmodel_news.text = text
        db.session.add(Tmodel_news)
        db.session.commit()
        return ops_renderJSON(msg="新闻文本修改成功！")
