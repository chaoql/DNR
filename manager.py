# -*- coding: utf-8 -*-
from application import app, db, manager
from flask_script import Server, Command
import traceback
import sys
from job.deepLearning import seeRawData_, downloadData, dataProcessSave, paramsSave, saveFeature
from www import *
import flask

# web server命令管理 (自定义启动命令)
# 运行命令：python manager.py runserver
manager.add_command("runserver", Server(host="0.0.0.0", use_debugger=True, use_reloader=False, port=8080))

# 下载原始数据，运行命令：python manager.py downloadData
manager.add_command("downloadData", downloadData)

# 查看原始数据，运行命令：python manager.py seeRawData
manager.add_command("seeRawData", seeRawData_)

# 原始数据处理并保存，运行命令：python manager.py dataProcessSave
manager.add_command("dataProcessSave", dataProcessSave)

# 保存模型参数，运行命令：python manager.py paramsSave
manager.add_command("paramsSave", paramsSave)

# 保存特征，运行命令：python manager.py saveFeature
manager.add_command("saveFeature", saveFeature)


def main():
    manager.run()


if __name__ == "__main__":
    # app.run( host = "0.0.0.0",debug=True )
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc()
