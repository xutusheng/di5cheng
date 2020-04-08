from selenium import webdriver
import unittest


class TestLogin(unittest.TestCase):
    """货主登录"""
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(r"d:\chrome\chromedriver.exe")
        cls.driver.get("http://58.213.75.35:9528/#/login")
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        pass

    def tearDown(self):
        self.driver.refresh()

    def test_01(self):
        username = self.driver.find_element_by_name("mobile")
        username.clear()
        username.send_keys("19951944242")
        password = self.driver.find_element_by_name("password")
        password.clear()
        password.send_keys("123456789")
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div/form/div[4]/div/button/span').click()
        text = self.driver.find_element_by_xpath("/html/body/div[2]/p").text
        self.assertEqual(text, "货主不存在")

    def test_02(self):
        username = self.driver.find_element_by_name("mobile")
        username.clear()
        username.send_keys("")
        password = self.driver.find_element_by_name("password")
        password.clear()
        password.send_keys("")
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div/form/div[4]/div/button/span').click()
        text = self.driver.find_element_by_xpath("//form/div[1]/div/div[2]").text
        self.assertEqual(text, "请输入正确的手机号")

    def test_03(self):
        username = self.driver.find_element_by_name("mobile")
        username.clear()
        username.send_keys("19951944242")
        password = self.driver.find_element_by_name("password")
        password.clear()
        password.send_keys("123456")
        self.driver.find_element_by_xpath('//*[@id="app"]/div/div/form/div[4]/div/button/span').click()
        text = self.driver.find_element_by_class_name("toggle-bar").text
        self.assertEqual(text, "爱优卫货主")


if __name__ == "__main__":
    unittest.main(verbosity=2)
