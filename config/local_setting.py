# 本地配置

"""
数据库链接
"""
SQLALCHEMY_DATABASE_URI = "mysql://root:cql666@localhost:3306/news_recommendation_system"

'''
相对地址转化为绝对地址
'''
# 手机热点或断网
# DOMAIN = {
#     'www': "http://192.168.43.214:8080/"
# }

# 家里wifi
DOMAIN = {
    'www': "http://192.168.0.102:8080/"
}

'''
版本控制
'''
# RELEASE_PATH = "D:/PythonWork/flaskProject_1/movie_cat/release_version"
