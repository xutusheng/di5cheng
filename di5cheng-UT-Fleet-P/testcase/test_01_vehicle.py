# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/10/10
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : test_01_vehicle.py

import allure
import pytest

from config import setting
from pages import pageView
from common.makeDir import *
from common.logger import log
from common.ParseYaml import ParseYaml
from common.ParseExcel import excel
from common.screenshot import screen_shot
from appium.webdriver.common.mobileby import By


allData = ParseYaml(setting.TEST_Element_YAML + '/' + 'vehicle.yaml')
reuseData = ParseYaml(setting.TEST_Element_YAML + '/' + 'reuse.yaml')

vehicles = excel.get_col_value(u"运力信息", 1)
m = len(vehicles) - 1
while vehicles[m] is None:
    m -= 1
last_vehicle = vehicles[m]
new_vehicle = last_vehicle[:2] + str(int(last_vehicle[2:]) + 1)
excel.write_cell(u"运力信息", m+3, 1, new_vehicle)


@pytest.mark.usefixtures("init")
@allure.feature("运力管理")
class TestVehicle:
    """
    测试新增车辆模块
    """
    @allure.story("新增车辆")
    @allure.severity("blocker")
    def test_new_vehicle(self, init):
        """新增一个车辆"""
        self.driver = init
        try:
            log.info("-----> 开始新增车辆")
            self.driver.find_element(By.ID, allData.get_element_info(0)).click()
            self.driver.find_element(By.ID, allData.get_element_info(1)).click()
            self.driver.find_element(By.ID, allData.get_element_info(2)).click()
            self.driver.find_element(By.ID, allData.get_element_info(3)).send_keys(new_vehicle)
            self.driver.find_element(By.ID, allData.get_element_info(4)).click()
            self.driver.find_element(By.ID, allData.get_element_info(5)).click()
            self.driver.find_element(By.ID, allData.get_element_info(6)).click()
            j = 0
            for i in range(3):
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
            j = 0
            for i in range(3):
                self.driver.find_elements(By.XPATH, reuseData.get_element_info(0))[j].click()
                self.driver.find_element(By.ID, reuseData.get_element_info(1)).click()
                self.driver.find_elements(By.ID, reuseData.get_element_info(2))[0].click()
                time.sleep(1)
                pageView.adb_tap((110, 260))
                time.sleep(1)
                pageView.adb_tap((668, 46))
                j += 1
            self.driver.find_element(By.ID, reuseData.get_element_info(6)).send_keys(new_vehicle[1:])
            pageView.wipe_up(self.driver)
            time.sleep(1)
            self.driver.find_elements(By.XPATH, reuseData.get_element_info(0))[j - 1].click()
            self.driver.find_element(By.ID, reuseData.get_element_info(1)).click()
            self.driver.find_elements(By.ID, reuseData.get_element_info(2))[0].click()
            time.sleep(1)
            pageView.adb_tap((110, 260))
            time.sleep(1)
            pageView.adb_tap((668, 46))
            self.driver.find_element(By.ID, reuseData.get_element_info(3)).click()
            self.driver.find_element(By.ID, reuseData.get_element_info(4)).click()
            self.driver.find_element(By.ID, reuseData.get_element_info(5)).click()
            self.driver.find_element(By.ID, reuseData.get_element_info(7)).click()
            time.sleep(5)
        except Exception as e:
            log.error("异常情况，返回错误信息是->: {0}".format(e))
            screen_shot(self.driver, allData.get_id() + '.png')


if __name__ == '__main__':
    pytest.main(['-s', '-q', '--alluredir', '../report/xml', 'test_01_vehicle.py'])
