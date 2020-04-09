# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/10/10
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : test_04_supercargo.py

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


allData = ParseYaml(setting.TEST_Element_YAML + '/' + 'supercargo.yaml')
reuseData = ParseYaml(setting.TEST_Element_YAML + '/' + 'reuse.yaml')

supercargoes = excel.get_col_value(u"运力信息", 5)
m = len(supercargoes) - 1
while supercargoes[m] is None:
    m -= 1
last_supercargo = supercargoes[m]
new_supercargo = last_supercargo[:4] + str(int(last_supercargo[4:]) + 1)
excel.write_cell(u"运力信息", m+3, 5, new_supercargo)

supercargoes_num = excel.get_col_value(u"运力信息", 6)
n = len(supercargoes_num) - 1
while supercargoes_num[n] is None:
    n -= 1
last_supercargo_num = supercargoes_num[n]
new_supercargo_num = last_supercargo_num + 1
excel.write_cell(u"运力信息", n+3, 6, new_supercargo_num)


@pytest.mark.usefixtures("init")
@allure.feature("运力管理")
class TestSupercargo:
    """
    测试新增押运员模块
    """
    @allure.story("新增押运员")
    @allure.severity("minor")
    def test_new_supercargo(self, init):
        """新增一个押运员"""
        self.driver = init
        try:
            log.info("-----> 开始新增押运员")
            self.driver.find_element(By.ID, allData.get_element_info(0)).click()
            self.driver.find_element(By.ID, allData.get_element_info(1)).click()
            self.driver.find_elements(By.ID, allData.get_element_info(2))[1].click()
            self.driver.find_element(By.ID, allData.get_element_info(3)).click()
            self.driver.find_element(By.ID, allData.get_element_info(4)).send_keys(new_supercargo)
            self.driver.find_element(By.ID, allData.get_element_info(5)).send_keys(new_supercargo_num)
            self.driver.find_element(By.ID, allData.get_element_info(6)).click()
            self.driver.find_element(By.XPATH, reuseData.get_element_info(0)).click()
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
            time.sleep(3)
        except Exception as e:
            log.error("异常情况，返回错误信息是->: {0}".format(e))
            screen_shot(self.driver, allData.get_id() + '.png')


if __name__ == '__main__':
    pytest.main(['-s', '-q', '--alluredir', '../report/xml', 'test_04_supercargo.py'])
