# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/9/30
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : pageView.py

import os
import yaml

from config import setting
from common.logger import log
from common.ParseYaml import ParseYaml
from appium.webdriver.common.mobileby import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


try:
    f = open(setting.TEST_DATA_YAML + '/' + 'login_data.yaml', encoding='utf-8')
    testData = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError as file:
    log.error("文件不存在：{0}".format(file))

allData = ParseYaml(setting.TEST_Element_YAML + '/' + 'login.yaml')


def user_login(driver):
    try:
        driver.find_element(By.ID, allData.get_element_info(0)).clear()
        driver.find_element(By.ID, allData.get_element_info(0)).send_keys(testData[5]['data']['username'])
        driver.find_element(By.ID, allData.get_element_info(1)).send_keys(testData[5]['data']['password'])
        driver.find_element(By.ID, allData.get_element_info(2)).click()
    except NoSuchElementException:
        log.error("异常登录，未找到登录页面元素！")


def user_logout(driver):
    try:
        driver.find_element(By.ID, allData.get_element_info(3)).click()
        driver.find_element(By.ID, allData.get_element_info(4)).click()
        driver.find_element(By.ID, allData.get_element_info(5)).click()
        driver.find_element(By.ID, allData.get_element_info(6)).click()
    except NoSuchElementException:
        log.error("异常退出，未找到主页面“我的”元素！")


def wipe_up(driver, t=500, n=1):
    """向上滑动屏幕"""
    size = driver.get_window_size()
    x1 = size['width'] * 0.5
    y1 = size['height'] * 0.50
    y2 = size['height'] * 0.25
    for i in range(n):
        driver.swipe(x1, y1, x1, y2, t)


def wipe_down(driver, t=500, n=1):
    """向下滑动屏幕"""
    size = driver.get_window_size()
    x1 = size['width'] * 0.5
    y1 = size['height'] * 0.25
    y2 = size['height'] * 0.75
    for i in range(n):
        driver.swipe(x1, y1, x1, y2, t)


def wipe_left(driver, t=500, n=1):
    """向左滑动屏幕"""
    size = driver.get_window_size()
    x1 = size['width'] * 0.75
    y1 = size['height'] * 0.5
    x2 = size['width'] * 0.25
    for i in range(n):
        driver.swipe(x1, y1, x2, y1, t)


def wipe_right(driver, t=500, n=1):
    """向右滑动屏幕"""
    size = driver.get_window_size()
    x1 = size['width'] * 0.25
    y1 = size['height'] * 0.5
    x2 = size['width'] * 0.75
    for i in range(n):
        driver.swipe(x1, y1, x2, y1, t)


def touch_tap(driver, x, y, duration=100):
    """
    method explain:点击坐标
    parameter explain：【x,y】坐标值,【duration】:决定点击的速度
    Usage: device.touch_coordinate(140,400)
    """
    screen_width = driver.get_window_size()['width']
    screen_height = driver.get_window_size()['height']
    a = (float(x) / screen_width) * screen_width
    x1 = int(a)
    b = (float(y) / screen_height) * screen_height
    y1 = int(b)
    driver.tap([(x1, y1), (x1, y1)], duration)


def adb_tap(args):
    """
    method explain:调用adb shell命令点击Android屏幕
    parameter explain：【args】坐标元祖
    Usage:adb_tap(140,400)
    """
    os.system('adb shell input tap {0} {1}'.format(*args))


def find_element(driver, loc):
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(loc))
