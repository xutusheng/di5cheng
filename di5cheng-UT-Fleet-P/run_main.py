# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/9/30
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : run_main.py

import pytest
import subprocess

from common.ParseConfig import xmlPath, htmlPath


def invoke(md):
    output, errors = subprocess.Popen(md, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    o = output.decode("utf-8")
    return o


if __name__ == '__main__':
    pytest.main(['-s', '-q', '--alluredir', xmlPath])
    # cmd = 'allure generate %s -o %s' % (xmlPath, htmlPath)
    # invoke(cmd)
