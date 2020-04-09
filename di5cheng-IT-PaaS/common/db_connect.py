# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/3
# @PROJECT : di5cheng-IT-PaaS
# @File    : db_connect.py

import pymysql
from sshtunnel import SSHTunnelForwarder


def ssh_connect():
    # ssh配置
    ssh_host = '******'
    ssh_username = "******"
    ssh_password = "******"
    remote_bind_address = "******"

    server = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username=ssh_username,
        ssh_password=ssh_password,
        remote_bind_address=(remote_bind_address, 3306))
    return server


def mysql_connect(server):
    db_url = "127.0.0.1"
    db_user = "******"
    db_password = "******"
    db_name = "d5c_auv"
    db = pymysql.connect(
        host=db_url,
        user=db_user,
        passwd=db_password,
        db=db_name,
        port=server.local_bind_port)
    return db
