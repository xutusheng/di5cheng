# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/10/10
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : test_05_bind.py

import allure
import pytest

from config import setting
from common.logger import log
from common.ParseYaml import ParseYaml
from common.screenshot import screen_shot
from appium.webdriver.common.mobileby import By

allData = ParseYaml(setting.TEST_Element_YAML + '/' + 'bind.yaml')


@allure.feature("运力管理")
class TestBind:
    """
    测试车辆司机绑定模块
    """
    def twice(self, index):
        for i in range(2):
            self.driver.find_element(By.ID, allData.get_element_info(index)).click()

    def delete(self):
        self.driver.find_element(By.ID, allData.get_element_info(12)).click()
        self.driver.find_element(By.ID, allData.get_element_info(8)).click()
        self.driver.find_element(By.ID, allData.get_element_info(9)).click()

    @allure.story("车辆司机绑定")
    @allure.severity("trivial")
    @pytest.mark.usefixtures("init")
    def test_new_bind(self, init):
        """新增车辆司机绑定"""
        self.driver = init
        try:
            log.info("-----> 开始车辆司机绑定")
            self.driver.find_element(By.ID, allData.get_element_info(0)).click()
            self.driver.find_element(By.ID, allData.get_element_info(1)).click()
            self.driver.find_element(By.ID, allData.get_element_info(2)).click()
            self.twice(3)
            self.twice(4)
            self.driver.find_element(By.ID, allData.get_element_info(5)).click()
            self.driver.find_element(By.ID, allData.get_element_info(3)).click()
            self.driver.find_element(By.ID, allData.get_element_info(6)).click()
            self.driver.find_element(By.ID, allData.get_element_info(3)).click()
            self.driver.find_element(By.ID, allData.get_element_info(7)).click()
            log.info("-----> 解除车辆司机绑定")
            self.driver.find_element(By.ID, allData.get_element_info(3)).click()
            self.driver.find_element(By.ID, allData.get_element_info(8)).click()
            self.driver.find_element(By.ID, allData.get_element_info(9)).click()
            self.driver.find_element(By.ID, allData.get_element_info(10)).click()
            log.info("-----> 开始删除车辆")
            self.driver.find_element(By.ID, allData.get_element_info(11)).click()
            self.driver.find_element(By.ID, allData.get_element_info(3)).click()
            self.delete()
            log.info("-----> 开始删除挂车")
            self.driver.find_elements(By.ID, allData.get_element_info(13))[1].click()
            self.driver.find_element(By.ID, allData.get_element_info(3)).click()
            self.delete()
            self.driver.find_element(By.ID, allData.get_element_info(14)).click()
            log.info("-----> 开始删除司机")
            self.driver.find_element(By.ID, allData.get_element_info(15)).click()
            self.driver.find_element(By.ID, allData.get_element_info(3)).click()
            self.delete()
            log.info("-----> 开始删除押运员")
            self.driver.find_elements(By.ID, allData.get_element_info(13))[1].click()
            self.driver.find_element(By.ID, allData.get_element_info(3)).click()
            self.delete()
        except Exception as e:
            log.error("异常情况，返回错误信息是->: {0}".format(e))
            screen_shot(self.driver, allData.get_id() + '.png')


if __name__ == '__main__':
    pytest.main(['-s', '-q', '--alluredir', '../report/xml', 'test_05_bind.py'])
