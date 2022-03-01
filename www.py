# -*- coding: utf-8 -*-
from flask_debugtoolbar import DebugToolbarExtension  # 调试工具:侧边栏
from interceptors.errorHandler import *  # 错误处理器
from controllers.index import index_page
from controllers.member import member_page
from common.libs.FLHelper.UrlManager import UrlManager
from interceptors.Auth import *

toolbar = DebugToolbarExtension(app)  # 调试模式

app.register_blueprint(index_page, url_prefix="/")  # 蓝图
app.register_blueprint(member_page, url_prefix="/member")  # 蓝图


# 模板函数
app.add_template_global(UrlManager.buildUrl, "buildUrl")
app.add_template_global(UrlManager.buildStaticUrl, "buildStaticUrl")
