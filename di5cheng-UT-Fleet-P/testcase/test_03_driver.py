# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/10/10
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : test_03_driver.py

import allure
import pytest
import time

from config import setting
from pages import pageView
from common.logger import log
from common.ParseYaml import ParseYaml
from common.ParseExcel import excel
from common.screenshot import screen_shot
from appium.webdriver.common.mobileby import By


allData = ParseYaml(setting.TEST_Element_YAML + '/' + 'driver.yaml')
reuseData = ParseYaml(setting.TEST_Element_YAML + '/' + 'reuse.yaml')

drivers = excel.get_col_value(u"运力信息", 3)
m = len(drivers) - 1
while drivers[m] is None:
    m -= 1
last_driver = drivers[m]
new_driver = last_driver[:4] + str(int(last_driver[4:]) + 1)
excel.write_cell(u"运力信息", m+3, 3, new_driver)

drivers_num = excel.get_col_value(u"运力信息", 4)
n = len(drivers_num) - 1
while drivers_num[n] is None:
    n -= 1
last_driver_num = drivers_num[n]
new_driver_num = last_driver_num + 1
excel.write_cell(u"运力信息", n+3, 4, new_driver_num)


@pytest.mark.usefixtures("init")
@allure.feature("运力管理")
class TestDriver:
    """
    测试新增司机模块
    """
    @allure.story("新增司机")
    @allure.severity("normal")
    def test_new_driver(self, init):
        """新增一个司机"""
        self.driver = init
        try:
            log.info("-----> 开始新增司机")
            self.driver.find_element(By.ID, allData.get_element_info(0)).click()
            self.driver.find_element(By.ID, allData.get_element_info(1)).click()
            self.driver.find_element(By.ID, allData.get_element_info(2)).click()
            self.driver.find_element(By.ID, allData.get_element_info(3)).send_keys(new_driver)
            self.driver.find_element(By.ID, allData.get_element_info(4)).send_keys("533323201803186311")
            self.driver.find_element(By.ID, allData.get_element_info(5)).send_keys(new_driver_num)
            self.driver.find_element(By.ID, allData.get_element_info(6)).click()
            j = 0
            for i in range(2):
                self.driver.find_elements(By.XPATH, reuseData.get_element_info(0))[j].click()
                self.driver.find_element(By.ID, reuseData.get_element_info(1)).click()
                self.driver.find_elements(By.ID, reuseData.get_element_info(2))[0].click()
                time.sleep(1)
                pageView.adb_tap((110, 260))
                time.sleep(1)
                pageView.adb_tap((668, 46))
                j += 1
            self.driver.find_element(By.ID, reuseData.get_element_info(3)).click()
            self.driver.find_element(By.ID, reuseData.get_element_info(4)).click()
            self.driver.find_element(By.ID, reuseData.get_element_info(5)).click()
            self.driver.find_element(By.ID, allData.get_element_info(7)).click()
            self.driver.find_elements(By.XPATH, reuseData.get_element_info(0))[0].click()
            self.driver.find_element(By.ID, reuseData.get_element_info(1)).click()
            self.driver.find_elements(By.ID, reuseData.get_element_info(2))[0].click()
            time.sleep(1)
            pageView.adb_tap((110, 260))
            time.sleep(1)
            pageView.adb_tap((668, 46))
            self.driver.find_element(By.ID, allData.get_element_info(8)).send_keys(new_driver_num)
            self.driver.find_element(By.ID, reuseData.get_element_info(3)).click()
            self.driver.find_element(By.ID, reuseData.get_element_info(4)).click()
            self.driver.find_element(By.ID, reuseData.get_element_info(5)).click()
            self.driver.find_element(By.ID, reuseData.get_element_info(7)).click()
            time.sleep(3)
        except Exception as e:
            log.error("异常情况，返回错误信息是->: {0}".format(e))
            screen_shot(self.driver, allData.get_id() + '.png')


if __name__ == '__main__':
    pytest.main(['-s', '-q', '--alluredir', '../report/xml', 'test_03_driver.py'])
