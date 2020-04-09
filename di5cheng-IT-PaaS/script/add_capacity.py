# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/5
# @PROJECT : di5cheng-IT-AUV
# @File    : add_capacity.py

import random
import asyncio
import requests
from common import config
from common import provide_data
from common.logger import MyLog

null = None

fleet_url = config.get_url()


def user_login_web(username, password):
    password_md5 = config.get_md5(password)
    url = fleet_url + 'paas/mm/userlogin?md=10&cmd=01'
    param = {
        "a": username,
        "b": password_md5
    }
    r = requests.post(url=url, json=param)
    response = eval(r.text)
    MyLog().logger().info(response)
    token, user_id = response['k'], response['b']
    return token, str(user_id)


def get_user_info(*args):
    url = fleet_url + 'saas/res/org/userInfo'
    headers = {
        'token': args[0],
        'user_id': args[1]
    }
    r = requests.post(url=url, headers=headers)
    response = eval(r.text)
    MyLog().logger().info(response)
    company_id = response['d']['f']
    return company_id


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


async def add_vehicle(fleet_user_id, fleet_id):
    """新增车辆"""
    global null
    vehicle_num = provide_data.get_info('车辆')
    url = fleet_url + 'saas/res/car/add'
    param = {
        'a': vehicle_num,
        'b': 1,
        'd': 'JA65E76231074EEC048',
        'e': 1747670400000,
        'f': 'JA65E76231074EEC048',
        'g': 'JA65E76231074EEC048',
        'h': 'JA65E76231074EEC048',
        'i': 'JA65E76231074EEC048',
        'j': 'JA65E76231074EEC048',
        'k': 'JA65E76231074EEC048',
        'l': 1747670400000,
        'n': fleet_id,
        'r': 1
    }
    result = post(fleet_user_id, url=url, param=param)
    assert result['a'] == '200'


async def add_trailer(fleet_user_id, fleet_id):
    """新增挂车"""
    global null
    trailer_num = provide_data.get_info('挂车')
    url = fleet_url + 'saas/res/car/add'
    param = {
        's': trailer_num,
        'c': random.randint(1, 5),
        'd': 'JA65E76231074EEC048',
        'e': 1747670400000,
        'f': 'JA65E76231074EEC048',
        'g': 'JA65E76231074EEC048',
        'h': 'JA65E76231074EEC048',
        'i': 'JA65E76231074EEC048',
        'j': 'JA65E76231074EEC048',
        'k': 'JA65E76231074EEC048',
        'l': 1747670400000,
        'm': trailer_num[1:-1],
        'n': fleet_id,
        'p': 33330,
        'q': '1',
        'r': 2
    }
    result = post(fleet_user_id, url=url, param=param)
    assert result['a'] == '200'


async def add_driver(fleet_user_id, fleet_id):
    """新增司机"""
    global null
    driver_info = provide_data.get_info('司机')
    url = fleet_url + 'saas/res/driver/add'
    param = {
        'a': fleet_id,
        'b': driver_info[0],
        'c': driver_info[2],
        'd': driver_info[1],
        'e': 'JE0B1F519007645B646',
        'f': 'JE0B1F519007645B646',
        'g': 1747670400000,
        'h': 'JE0B1F519007645B646',
        'i': 1747670400000,
        'j': str(driver_info[1]),
        'm': 1
    }
    result = post(fleet_user_id, url=url, param=param)
    assert result['a'] == '200'


async def add_supercargo(fleet_user_id, fleet_id):
    """新增押运员"""
    global null
    supercargo_info = provide_data.get_info('押运员')
    url = fleet_url + 'saas/res/driver/add'
    param = {
        'a': fleet_id,
        'b': supercargo_info[0],
        'd': supercargo_info[1],
        'k': 'JE0B1F519007645B646',
        'l': 1747670400000,
        'm': 2
    }
    result = post(fleet_user_id, url=url, param=param)
    assert result['a'] == '200'


def add_bind(fleet_user_id, fleet_id):
    """新增运力"""
    url = fleet_url + 'saas/res/transport/add'
    param = {
        'a': fleet_id,
        'b': '车辆ID',
        'c': '挂车ID',
        'd': '司机ID',
        'e': '司机UID',
        'f': '押运员ID',
        'g': ''
    }
    result = post(fleet_user_id, url=url, param=param)
    assert result['a'] == '200'


def main(username, password):
    fleet_user_id = user_login_web(username, password)
    fleet_id = get_user_info(*fleet_user_id)
    coroutine1 = add_vehicle(fleet_user_id, fleet_id)
    coroutine2 = add_trailer(fleet_user_id, fleet_id)
    coroutine3 = add_driver(fleet_user_id, fleet_id)
    coroutine4 = add_supercargo(fleet_user_id, fleet_id)
    tasks = [asyncio.ensure_future(coroutine1),
             asyncio.ensure_future(coroutine2),
             asyncio.ensure_future(coroutine3),
             asyncio.ensure_future(coroutine4)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    main(19933334444, '123456')
