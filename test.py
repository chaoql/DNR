import base64
import string
import random

pwd = "123"
keyList = [random.choice((string.ascii_letters + string.digits)) for i in range(8)]
salt = "".join(keyList)
print(salt)
print(pwd)
print(pwd.encode("utf-8"))
print(base64.encodebytes(pwd.encode("utf-8")))
print(base64.encodebytes(pwd))
str = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
print(str)