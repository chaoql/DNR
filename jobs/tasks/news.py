import hashlib
import traceback
import time
from urllib.parse import urlparse

from common.models.news import News
import os
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from application import app, db
from common.libs.FLHelper.DateHelper import getCurrentTime

"""
python manager.py runjob -m news
"""


class JobTask:
    def __init__(self):
        self.date = getCurrentTime(frm="%Y%m%d")
        self.source = "puffpost"
        self.urls = ["https://new.qq.com/ch/antip/", "https://new.qq.com/ch/ent/", "https://new.qq.com/ch/milite/",
                     "https://new.qq.com/ch/world/", "https://new.qq.com/ch/tech/", "https://new.qq.com/ch/finance/ "]

    def run(self, params):
        self.getList()
        # self.parseInfo()

    def getList(self):
        """
        获取电影列表信息
        :return:None
        """
        app.logger.info("正在获取新闻列表信息...")
        for url in self.urls:  # 页面循环
            app.logger.info("get list: " + url)
            content = self.getHttpContent(url)  # 线上获取content操作时，必须关闭vpn
            time.sleep(0.3)
            items_data = self.parseList(content, url)  # 解析界面  获得[{单一电影的名字、详情网址}{...}{...}]型的信息
            if not items_data:
                continue
            for item in items_data:  # 单电影信息循环
                tmp_content = self.getHttpContent(item["url"])  # 单个电影详情页面的Content
                break
            break

    # def parseInfo(self):
    #     """
    #     解析详情界面的content
    #     :return:返回包含电影信息的字典的列表
    #     """
    #     app.logger.info("正在解析详情界面的content...")
    #     config = self.url
    #     path_root = config["path"] + self.date
    #     path_info = path_root + "/info"
    #     path_json = path_root + "/json"
    #     for filename in os.listdir(path_info):
    #         tmp_json_path = path_json + "/" + filename
    #         tmp_info_path = path_info + "/" + filename
    #         tmp_data = json.loads(self.getContent(tmp_json_path), encoding="utf-8")
    #         tmp_content = self.getContent(tmp_info_path)
    #         tmp_soup = BeautifulSoup(tmp_content, "html.parser")
    #         try:
    #             # tmp_name = tmp_soup.select("div.container div.article-container header.product-header "
    #             #                            "h1.product-title")[0].contents[0].__str__()  # 仅爬取当前文本，不含子节点文本
    #             tmp_pub_date = tmp_soup.select("div.container div.article-container header.product-header "
    #                                            "h1.product-title span")[0].getText().replace("(", "").replace(")", "")
    #             tmp_desc = tmp_soup.select("div.container div.article-container header.product-header "
    #                                        "div.product-excerpt span")[5].getText()
    #             tmp_classify = tmp_soup.select("div.container div.article-container header.product-header "
    #                                            "div.product-excerpt")[2].select("span a")
    #             tmp_actor = tmp_soup.select("div.container div.article-container header.product-header "
    #                                         "div.product-excerpt")[1].select("span a")
    #             tmp_cover_pic = tmp_soup.select("div.container div.article-container header.product-header img")[0][
    #                 "src"]
    #             tmp_actors = tmp_classifies = ""
    #             for i in range(len(tmp_classify)):
    #                 word = "" if i == (len(tmp_classify) - 1) else "/"
    #                 tmp_classifies += tmp_classify[i].getText() + word
    #             for i in range(len(tmp_actor)):
    #                 word = "" if i == len(tmp_classify) - 1 else "/"
    #                 tmp_actors += tmp_actor[i].getText() + word
    #             tmp_data["classify"] = "暂无分类" if tmp_classifies == "" else tmp_classifies
    #             tmp_data["actor"] = tmp_actors
    #             tmp_data["cover_pic"] = tmp_cover_pic
    #             tmp_data["desc"] = tmp_desc
    #             tmp_data["pub_date"] = tmp_pub_date
    #             tmp_data["updated_time"] = tmp_data["created_time"] = getCurrentTime(frm="%Y-%m-%d %H:%M:%S")
    #             tmp_data["source"] = self.source
    #             tmp_data["view_counter"] = 0
    #             # app.logger.info(tmp_data)
    #             # app.logger.info("***************************")
    #             tmp_movie_info = Movie.query.filter_by(hash=tmp_data["hash"]).first()
    #             if tmp_movie_info:
    #                 continue
    #             tmp_model_info = Movie(**tmp_data)
    #             db.session.add(tmp_model_info)
    #             db.session.commit()
    #         except Exception as e:
    #             traceback.print_exc()
    #     return True

    def parseList(self, content, url):
        """
        解析电影列表页面的content
        :param content: 待解析的页面Content
        :return: 包含电影名称和电影详情网址字典的列表
        """
        app.logger.info("正在解析新闻列表页面的content...")
        data = []
        url_info = urlparse(url)
        url_domain = url_info[0] + "://" + url_info[1]
        tmp_soup = BeautifulSoup(str(content), "html.parser")
        tmp_list = tmp_soup.select("div.List div.channel_mod #dataFull li.itme-ls")
        for item in tmp_list:
            tmp_target = item.select("a.picture")
            tmp_href = tmp_target[0]["href"]
            tmp_target = item.select("a.picture img")
            tmp_name = tmp_target[0]["alt"]
            tmp_pic = tmp_target[0]["src"]
            if "http:" not in tmp_href:
                tmp_href = url_domain + tmp_href
            tmp_data = {
                "name": tmp_name,
                "url": tmp_href,
                "pic": tmp_pic,
                "hash": hashlib.md5(tmp_href.encode("utf-8")).hexdigest()
            }
            # app.logger.info(tmp_data)
            data.append(tmp_data)
            app.logger.info(tmp_data)
            break
        return data

    @staticmethod
    def getHttpContent(url):
        """
        从线上获取页面content
        :param url: 页面网址
        :return: content
        """
        app.logger.info("正在从线上获取页面content...")
        try:
            r = requests.get(url=url)
            if r.status_code != 200:
                return None
            return r.content
        except Exception as e:
            traceback.print_exc()
            return None
