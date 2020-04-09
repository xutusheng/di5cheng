# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/9/30
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : screenshot.py

import os

from config import setting

if not os.path.exists(setting.REPORT_DIR):
    os.makedirs(setting.REPORT_DIR + '/' + "screenshot")
elif not os.path.exists(setting.REPORT_DIR + '/' + "screenshot"):
    os.makedirs(setting.REPORT_DIR + '/' + "screenshot")


def screen_shot(driver, file_name):
    """
    截图
    :param driver: 启动浏览器
    :param file_name: 截图文件名
    :return: 返回指定路径的截图文件
    """
    file_path = setting.REPORT_DIR + "/screenshot/" + file_name
    return driver.get_screenshot_as_file(file_path)
