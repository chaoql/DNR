from application import app
from common.libs.FLHelper.DateHelper import getCurrentTime
import os


class UrlManager(object):
    @staticmethod
    def buildUrl(path):
        """
        相对地址转化为绝对地址
        :param path:
        :return:
        """
        config_domain = app.config['DOMAIN']
        return "%s%s" % (config_domain['www'], path)

    @staticmethod
    def buildStaticUrl(path):
        """
        静态相对地址转化为绝对地址
        :param path:
        :return:
        """
        path = "/static" + path + "?ver=" + UrlManager.getReleaseVersion()
        return UrlManager.buildUrl(path)

    @staticmethod
    def getReleaseVersion():
        """
        版本管理
        开发模式：使用时间作为序列号
        生产环境：使用版本文件进行管理，覆盖开发模式的值
        :return:
        """
        ver = "%s" % (getCurrentTime("%Y%m%d%H%M%S%f"))
        release_path = app.config.get('RELEASE_PATH')
        if release_path and os.path.exists(release_path):
            with open(release_path, 'r') as f:
                ver = f.readline()
        return ver
