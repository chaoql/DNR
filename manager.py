# -*- coding: utf-8 -*-
from application import app, db, manager
from flask_script import Server, Command
import traceback
import sys
from www import *
import flask

# web server命令管理 (自定义启动命令)
# 运行命令：python manager.py runserver
manager.add_command("runserver", Server(host="0.0.0.0", use_debugger=True, use_reloader=False, port=8080))


def main():
    manager.run()


if __name__ == "__main__":
    # app.run( host = "0.0.0.0",debug=True )
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc()
