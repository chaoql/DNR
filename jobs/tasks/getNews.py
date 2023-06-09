import hashlib
import traceback
import time
import urllib
from urllib.parse import urlparse
from selenium import webdriver
from common.models.news import News
import os
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from application import app, db
from common.libs.FLHelper.DateHelper import getCurrentTime

"""
python manager.py runjob -m getNews
"""


class JobTask:
    def __init__(self):
        self.date = getCurrentTime(frm="%Y%m%d")
        self.source = "puffpost"
        self.urls = ["https://new.qq.com/ch/ent/", "https://new.qq.com/ch/milite/",
                     "https://new.qq.com/ch/world/", "https://new.qq.com/ch/tech/", "https://new.qq.com/ch/finance/ "]

    def run(self, params):
        self.getList()
        # self.parseInfo()

    def getList(self):
        """
        获取电影列表信息
        :return:None
        """
        app.logger.warning("正在获取新闻列表信息...")
        for url in self.urls:  # 页面循环
            app.logger.warning("get list: " + url)
            content = self.getHttpContent(url, flag="list")  # 线上获取content操作时，必须关闭vpn
            items_data = self.parseList(content, url)  # 解析界面  获得[{单一电影的名字、详情网址}{...}{...}]型的信息
            for item in items_data:  # 单电影信息循环
                tmp_content = self.getHttpContent(item["link"])  # 单个电影详情页面的Content
                self.parseInfo(tmp_content, item)

    def parseInfo(self, content, item):
        """
        解析详情界面的content
        :return:返回包含电影信息的字典的列表
        """
        app.logger.warning("正在解析详情界面的content...")
        soup = BeautifulSoup(str(content), "html.parser")
        try:
            tmp_text = soup.select("div.content-article p.one-p")
            print(tmp_text)
            item["text"] = ""
            for text in tmp_text:
                if text.select("img"):
                    continue
                item["text"] += text.getText()
            if item["text"] == "":
                app.logger.warning("网站无文本信息，跳过...")
                return False
            self.download_pics(item)
            app.logger.warning(item["text"])
            tmp_year = soup.select("div.year.through span")[0].getText()
            tmp_month_day = soup.select("div.md")[0].getText().replace("/", "-")
            tmp_time = soup.select("div.time")[0].getText() + ":00"
            tmp_date = tmp_year + "-" + tmp_month_day + " " + tmp_time
            item["date"] = tmp_date
            tmp_news_info = News.query.filter_by(hash=item["hash"]).first()
            item["view_counter"] = 0
            if tmp_news_info:
                return False
            tmp_model_info = News(**item)

            db.session.add(tmp_model_info)
            db.session.commit()
        except Exception as e:
            traceback.print_exc()
        return True

    def parseList(self, content, url):
        """
        解析新闻列表页面的content
        :param url:
        :param content: 待解析的页面Content
        :return: 包含电影名称和电影详情网址字典的列表
        """
        app.logger.warning("正在解析新闻列表页面的content...")
        data = []
        url_info = urlparse(url=url)
        url_domain = url_info[0] + "://" + url_info[1]
        tmp_soup = BeautifulSoup(str(content), "html.parser")
        tmp_list = tmp_soup.select("div#List div.channel_new ul#dataFull.list li.item.cf.itme-ls")
        for item in tmp_list:
            try:
                tmp_genre = url.split("/")[-2]
                tmp_target = item.select("a.picture")
                tmp_href = tmp_target[0]["href"]
                tmp_target = item.select("a.picture img")
                tmp_name = tmp_target[0]["alt"]
                tmp_pic = tmp_target[0]["src"]
                tmp_Authors = item.select("div.detail div.binfo.cf div.fl a.source")[0].getText()
                if len(tmp_Authors) == 0:
                    tmp_Authors = item.select("div.detail div.binfo.cf div.fl span.source")[0].getText()
                app.logger.warning(tmp_name)
                if "http:" not in tmp_href and "https:" not in tmp_href:
                    tmp_href = url_domain + tmp_href
                tmp_data = {
                    "title": tmp_name,
                    "link": tmp_href,
                    "photo": tmp_pic,
                    "hash": hashlib.md5(tmp_href.encode("utf-8")).hexdigest(),
                    "authors": tmp_Authors,
                    "genres": tmp_genre
                }
                data.append(tmp_data)
            except Exception as e:
                traceback.print_exc()
        app.logger.warning(data)
        return data

    @staticmethod
    def getHttpContent(url, flag=""):
        """
        从线上获取页面content
        :param flag:
        :param url: 页面网址
        :return: content
        """
        app.logger.warning("正在从线上获取页面content...")
        try:
            driver = webdriver.Chrome(
                executable_path="C:/Program Files/Google/Chrome/Application/chromedriver.exe")  # chromedriver的地址
            driver.get(url=url)
            if flag == "list":
                for i in range(1, 200):
                    time.sleep(0.5)
                    driver.execute_script("window.scrollTo(window.scrollX, %d);" % (i * 200))
            return driver.page_source
        except Exception as e:
            traceback.print_exc()
            return None

    def download_pics(self, item):
        f = open('E:/个人修行/毕业设计/dnr-bisher/static/images/news/' + str(item["hash"]) + ".jpg", 'wb')
        f.write((urllib.request.urlopen(item["photo"])).read())
        print("图片下载：" + item["photo"])
        f.close()
