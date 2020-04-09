# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/3
# @PROJECT : di5cheng-IT-PaaS
# @File    : main.py

import pytest
import os

if __name__ == "__main__":
    pytest.main(['-s', '-q', '--alluredir', './report/xml'])
    os.system('allure generate %s -o %s' % ('./report/xml', './report/html'))
