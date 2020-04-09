# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/17
# @PROJECT : di5cheng-IT-PaaS
# @File    : web.py

import requests
from common import config
from common.logger import MyLog

null = None


class Web:

    global null

    def __init__(self):
        self.url = config.get_url()

    def user_login_web(self, username, password):
        password_md5 = config.get_md5(password)
        url = self.url + 'paas/mm/userlogin?md=10&cmd=01'
        param = {
            "a": username,
            "b": password_md5
        }
        r = requests.post(url=url, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        token, user_id = response['k'], response['b']
        return token, str(user_id)

    def get_user_info(self, *args):
        url = self.url + 'saas/res/org/userInfo'
        headers = {
            'token': args[0],
            'user_id': args[1]
        }
        r = requests.post(url=url, headers=headers)
        response = eval(r.text)
        MyLog().logger().info(response)
        company_id = response['d']['f']
        return company_id

    @staticmethod
    def post(*args, url, param):
        headers = {
            'token': args[0],
            'user_id': args[1]
        }
        param = param
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def issue_inquiry(self, *args, param):
        # 发布询价
        url = self.url + 'saas/goods/inquiry/add'
        headers = {
            'token': args[0],
            'user_id': args[1]
        }
        param = param
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    @staticmethod
    def web_post(url, headers, param):
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    @staticmethod
    def service_confirm_car_post(*args, url, param):
        headers = {
            "token": args[0],
            "user_id": args[1],
            "cpy_id": "0",
            "dt_type": "1",
            "user_type": "4",
            "product_id": "2020",
            "op_code": "PG022",
            "op_ncode": "326:PT015"
        }
        param = param
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def confirm_inquiry(self, user_id, param):
        # 询价确认发货
        url = self.url + 'saas/inquiry/confirm/confirmInquiry'
        headers = {'user_id': str(user_id)}
        param = param
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def get_address(self, user_id, param):
        # 请求常用装卸货地址
        url = self.url + 'saas/goods/address/find'
        headers = {'user_id': str(user_id)}
        param = param
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def add_address(self, user_id, param):
        # 新增常用装卸货地址
        url = self.url + 'saas/res/address/addOrUpdate'
        headers = {'user_id': str(user_id)}
        param = param
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def userlogin(self, a, b):
        # 登录
        url = self.url + "paas/mm/userlogin?md=10&cmd=01"
        # 给密码进行MD5加密
        b_md5 = config.get_md5(b)
        param = {"a": a, "b": b_md5}
        r = requests.post(url=url, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def queryUserBasicInfo(self, user_id):
        # 查询用户基本信息
        url = self.url + "saas/res/org/userInfo"
        headers = {"user_id": str(user_id)}
        param = {}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response
