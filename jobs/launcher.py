import argparse
import importlib
import sys
import traceback
from flask_script import Command
from application import app
"""
job统一入口文件
python manager.py runjob -m Test (job/tasks/Test.py)
python manager.py runjob -m test/index (job/tasks/test/index.py)

"""


class runjob(Command):
    capture_all_args = True

    def run(self, *args, **kwargs):
        # print(sys.argv)  # ['manager.py', 'runjob']
        app.logger.info("sssssssssssss")
        args = sys.argv[2:]
        parser = argparse.ArgumentParser(add_help=True)  # 解析器
        parser.add_argument("-m", "--name", dest="name", metavar="name", help="指定job名", required=True)
        parser.add_argument("-a", "--act", dest="act", metavar="act", help="Job动作", required=False)
        parser.add_argument("-p", "--param", dest="param", nargs="*", metavar="param", help="业务参数", required=False)
        params = parser.parse_args(args)
        params_dict = params.__dict__
        if "name" not in params_dict or not params_dict["name"]:
            return self.tips()
        try:
            """
            from jobs.tasks.test import JobTask
            """
            module_name = params_dict["name"].replace("/", ".")
            import_string = "jobs.tasks.%s" % module_name
            target = importlib.import_module(import_string)
            exit(target.JobTask().run(params_dict))
        except Exception as e:
            traceback.print_exc()
        return

    def tips(self):
        tip_msg = """
        请正确的调度JOB
        python manager.py runjob -m Test (job/tasks/Test.py)
        python manager.py runjob -m test/index (job/tasks/test/index.py)
        """
        print(tip_msg)
        return
