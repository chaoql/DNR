import base64
import hashlib
import random
import string


class UserService:
    """
    产生md5加密后的密码
    因为存在随机的salt,所以即使密码相同，加密后的密码也一定不一样
    """
    @staticmethod
    def genePwd(pwd, salt):
        m = hashlib.md5()
        str = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def geneAuthCode(user_info=None):
        m = hashlib.md5()
        str = "%s-%s-%s-%s-%s" % (user_info.id, user_info.login_name,
                                  user_info.login_pwd, user_info.login_salt, user_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        keyList = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return "".join(keyList)
