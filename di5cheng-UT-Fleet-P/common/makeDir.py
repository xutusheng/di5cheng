# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/10/10
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : makeDir.py

import os
import time

from common.logger import log


def mk_dir(path):

    is_exists = os.path.exists(path)

    if not is_exists:
        try:
            os.makedirs(path)
        except Exception as e:
            log.error("%s目录创建失败：%s" % (str(path), e))

    now = time.strftime("%Y-%m-%d %H_%M_%S")

    os.mkdir(path + "\\" + str(now))


def get_new_dir(path):
    """获取最新的测试报告"""
    lists = os.listdir(path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(path, fn)))
    new_dir = os.path.join(path, lists[-1])
    return new_dir
