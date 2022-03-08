from time import time
from application import app
import jwt
from common.models.user import User


def get_token():
    context = jwt.encode({'reset_pwd': 10, 'exp': time()}, app.config['SECRET_KEY'],
                         algorithm='HS256')
    print(context)
    return context


def verify_token(token):
    id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_pwd']
    print(int(id))


print(verify_token(get_token()))