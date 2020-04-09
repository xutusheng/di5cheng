# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/16
# @PROJECT : di5cheng-IT-PaaS
# @File    : test_app.py

from ctypes import *
from api import app
from common import config

null = None


class TestCase:

    global null

    def setup_class(self):
        self.library = cdll.LoadLibrary(config.get_library())
        self.app = app.Common()
        self.app.initSDK(library=self.library, init_info=config.get_app_url())

        # app登录
        login_info = self.app.app_login(library=self.library, username=19933330000, password=123456)
        self.dispatch_user_id = eval(login_info["pBody"])["i"]

    def test_case01(self):
        self.app.trans_manifest_list(library=self.library, x=1, y=1)
