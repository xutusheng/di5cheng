# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/10/10
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : login.py

import yaml
import pytest

from config import setting
from common.logger import log
from common.ParseYaml import ParseYaml
from common.screenshot import screen_shot
from appium.webdriver.common.mobileby import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


try:
    f = open(setting.TEST_DATA_YAML + '/' + 'login_data.yaml', encoding='utf-8')
    testData = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError as file:
    log.error("文件不存在：{0}".format(file))

allData = ParseYaml(setting.TEST_Element_YAML + '/' + 'login.yaml')

data = (["", ""],
        ["", "123456"],
        ["15252162668", ""],
        ["17751515555", "123456"],
        ["15252162668", "147852"],
        ["15252162668", "123456"])

data_ids = ["{0},{1}".format(d[0], d[1]) for d in data]


@pytest.mark.parametrize(["username", "password"], data, ids=data_ids)
class TestLogin:
    """
    测试登录模块
    """
    def user_login(self, username, password):
        self.driver.find_element(By.ID, allData.get_element_info(0)).clear()
        self.driver.find_element(By.ID, allData.get_element_info(0)).send_keys(username)
        self.driver.find_element(By.ID, allData.get_element_info(1)).send_keys(password)
        self.driver.find_element(By.ID, allData.get_element_info(2)).click()

    def user_logout(self):
        self.driver.find_element(By.ID, allData.get_element_info(3)).click()
        self.driver.find_element(By.ID, allData.get_element_info(4)).click()
        self.driver.find_element(By.ID, allData.get_element_info(5)).click()
        self.driver.find_element(By.ID, allData.get_element_info(6)).click()

    def test_login(self, data_yaml):
        """
        登录测试
        :param data_yaml: 加载login_data登录测试数据
        :return:
        """
        log.info("当前执行测试用例ID-> {0} ; 测试点-> {1}".format(data_yaml['id'], data_yaml['detail']))
        self.user_login(data_yaml['data']['username'], data_yaml['data']['password'])
        # time.sleep(3)
        try:
            if data_yaml['screenShot'] == "usn_psw_right":
                login_element = WebDriverWait(self.driver, 5).until(lambda x: x.find_element(
                    By.ID, allData.get_check_element_info(0)))
                self.assertTrue(login_element)
                log.info("登录成功，判断依据是->: {0}".format('找到我的元素'))
                log.info("-----> 开始执行退出流程操作")
                self.user_logout()
                logout_element = WebDriverWait(self.driver, 5).until(lambda x: x.find_element(
                    By.ID, allData.get_check_element_info(1)))
                logout_msg = logout_element.text
                log.info("退出成功，判断依据是->: {0}".format(logout_msg))

            elif data_yaml['screenShot'] == "psw_error":
                toast_loc = ("xpath", allData.get_check_element_info(2))
                toast_el = WebDriverWait(self.driver, 5, 0.01).until(ec.presence_of_element_located(toast_loc))
                self.assertTrue(toast_el)
                log.info("登录失败，判断依据是->: {0}".format(allData.get_check_element_info(2)))

            elif data_yaml['screenShot'] == "usn_psw_empty" or data_yaml['screenShot'] == "usn_empty":
                toast_loc = ("xpath", allData.get_check_element_info(3))
                toast_el = WebDriverWait(self.driver, 5, 0.01).until(ec.presence_of_element_located(toast_loc))
                self.assertTrue(toast_el)
                log.info("登录失败，判断依据是->: {0}".format(allData.get_check_element_info(3)))

            else:
                toast_loc = ("xpath", allData.get_check_element_info(4))
                toast_el = WebDriverWait(self.driver, 5, 0.01).until(ec.presence_of_element_located(toast_loc))
                self.assertTrue(toast_el)
                log.info("登录失败，判断依据是->: {0}".format(allData.get_check_element_info(4)))

        except Exception as e:
            log.error("异常情况，返回错误信息是->: {0}".format(e))
            screen_shot(self.driver, data_yaml['screenShot'] + '.png')


if __name__ == '__main__':
    pytest.main(['-s', '-q', '--alluredir', '../report/xml', 'test_00_login.py'])
