# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/9/30
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : setting.py

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

# 配置文件目录
CONFIG_DIR = os.path.join(BASE_DIR, "database", "user.ini")
# 测试用例目录
CASE_DIR = os.path.join(BASE_DIR, "testcase")
# 测试报告目录
REPORT_DIR = os.path.join(BASE_DIR, "report")
# 日志文件目录
LOG_DIR = os.path.join(BASE_DIR, "logs")
# 测试数据文件
TEST_DATA_YAML = os.path.join(BASE_DIR, "data", "testdata")
# 元素控件文件
TEST_Element_YAML = os.path.join(BASE_DIR, "data", "testyaml")
# word文件
WORD_DIR = os.path.join(BASE_DIR, "data", "word")
# excel文件
EXCEL_DIR = os.path.join(BASE_DIR, "data", "excel")
# HTML目录
HTML_DIR = os.path.join(BASE_DIR, "report", "html")
# XML目录
XML_DIR = os.path.join(BASE_DIR, "report", "xml")
