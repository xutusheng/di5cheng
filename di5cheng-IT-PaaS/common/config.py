# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/3
# @PROJECT : di5cheng-IT-PaaS
# @File    : config.py

import os
import hashlib
import configparser

# 获取config配置文件
path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
config_path = path + '\\config\\config.ini'

# 实例化configParser对象
config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')


def get_config(section, key):  # 根据标识和key获取相应的键值
    value = config.get(section, key)
    return value


def get_config_db(key):  # 获取数据库配置的相应键值
    value = config.get("db", key)
    return value


def get_config_log(key):  # 获取日志配置的相应键值
    value = config.get("log", key)
    return value


def get_config_driver():  # 获取浏览器配置的相应键值
    value = config.get("browser", "browserType")
    return value


def get_environment():
    value = config.get("environment", "Environmental")
    return value


def get_url():  # 获取url
    env = get_environment()
    value = config.get("url", "URL_" + env)
    return value


def get_app_url():  # 获取url
    env = get_environment()
    value = bytes(config.get("url", "INIT_" + env), encoding="utf-8")
    return value


def get_result():  # 运行结果是否保留的参数
    value = int(config.get("resport", "isClear"))
    return value


def get_server():
    Smtp_Server = config.get("email", "Smtp_Server")
    return Smtp_Server


def get_sender():
    Smtp_Sender = config.get("email", "Smtp_Server")
    return Smtp_Sender


def get_sender_pwd():
    Smtp_Sender_Password = config.get("email", "Smtp_Sender_Password")
    return Smtp_Sender_Password


def get_receiver():
    Smtp_Receiver = config.get("email", "Smtp_Receiver")
    return Smtp_Receiver


def get_account(account_type):
    value = eval(config.get("account", account_type))
    return value


def get_picture():
    value = config.get("picture", "JPG").split(",")
    return value


def get_excel():
    excel_path = path + config.get("excel", "excel_path")
    return excel_path


def get_excel_demo():
    excel_path = path + config.get("excel", "excel_demo_path")
    return excel_path


def get_word():
    word_path = path + config.get("word", "word_path")
    return word_path


def get_library(library=None):
    if library is None:
        library_path = path + config.get("library", "library_path")
    else:
        library_path = path + config.get("library", library)
    return library_path


def get_report_path():
    report_path = path + config.get("report", "report_path")
    return report_path


def get_md5(key):
    hl = hashlib.md5()
    hl.update(key.encode('utf-8'))
    key_md5 = hl.hexdigest()
    print(key, "  ---->  ", key_md5)
    return key_md5
