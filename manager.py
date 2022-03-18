# -*- coding: utf-8 -*-
from application import app, db, manager
from flask_script import Server, Command   # from ._compat import text_type 改成 from flask_script._compat import text_type
import traceback
import sys
from jobs.launcher import runjob
from www import *
import flask

# web server命令管理 (自定义启动命令)
# 运行命令：python manager.py runserver
manager.add_command("runserver", Server(host="localhost", use_debugger=True, use_reloader=False, port=8080))

# Job框架：python manager.py runjob
manager.add_command("runjob", runjob)


def main():
    manager.run()


if __name__ == "__main__":
    # app.run( host = "0.0.0.0",debug=True )
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc()
