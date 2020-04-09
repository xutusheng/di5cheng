# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/9/30
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : logger.py

import os
import time
import logging

from config import setting

if not os.path.exists(setting.LOG_DIR):
    os.mkdir(setting.LOG_DIR)


class Log:
    """
    日志记录类
    """
    def __init__(self):
        self.logname = os.path.join(setting.LOG_DIR, "%s.log" % time.strftime("%Y-%m-%d %H_%M_%S"))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter("[%(asctime)s] - %(filename)s - %(levelname)s: %(message)s")

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.logname, "a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == "info":
            self.logger.info(message)
        elif level == "debug":
            self.logger.debug(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        self.logger.removeHandler(fh)
        self.logger.removeHandler(ch)
        fh.close()

    def debug(self, message):
        self.__console("debug", message)

    def info(self, message):
        self.__console("info", message)

    def warning(self, message):
        self.__console("warning", message)

    def error(self, message):
        self.__console("error", message)


log = Log()
