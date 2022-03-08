# 共用配置
DEBUG = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf8mb4"
SECRET_KEY = "123456"
AUTH_COOKIE_NAME = "DNR"
SCHEDULER_TIMEZONE = "Asia/Shanghai"

# 表单配置
CSRF_ENABLED = True
SECRET_KEY = 'YOU-WILL-SUCCEED'

# 邮件发送
MAIL_SUPPRESS_SEND = False  # 默认为app.testing，如果为True，则不会真的发送邮件，供测试使用
MAIL_SERVER = 'smtp.126.com'       # 邮件服务器地址，默认为localhost
MAIL_PASSWORD = 'VGEBFVTCKBGXNNTL'  # 邮箱服务器授权码
MAIL_USERNAME = 'chaoql@126.com'  # 邮箱用户名
ADMINS = ['1415331985@qq.com']
# MAIL_PROT = 25,
# MAIL_USE_TSL = False,
# MAIL_USE_SSL = False,
# MAIL_DEBUG = True
# MAIL_SERVER = 'smtp.qq.com'       # 邮件服务器地址，默认为localhost
# MAIL_PASSWORD = 'hodvahanaabqbach'
# MAIL_USERNAME = '1415331985@qq.com'  # 邮箱用户名
# ADMINS = ['chaoql@126.com']
