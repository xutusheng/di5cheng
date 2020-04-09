# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/10/10
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : conftest.py

import pytest

from appium import webdriver


@pytest.fixture(scope="module")
def init():
    desired_caps = {'platformName': 'Android',
                    'platformVersion': '8',
                    'deviceName': 'SNMBB18413537671',
                    'appPackage': 'com.di5cheng.auv',
                    'appActivity': 'com.di5cheng.auv.WelcomeActivity',
                    'automationName': 'uiautomator2',
                    'unicodeKeyboard': True,
                    'resetKeyboard': True,
                    'noReset': True,
                    'newCommandTimeout': 60
                    }
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


if __name__ == '__main__':
    pytest.main(["-s", "conftest.py"])
