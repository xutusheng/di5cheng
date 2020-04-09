# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/9/30
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : ParseYaml.py

import yaml


class ParseYaml:
    """
    解析yaml文件数据类
    """
    def __init__(self, filepath):
        """
        :param filepath: 文件路径
        """
        self.path = filepath

    def get_yaml(self):
        """
        加载yaml文件数据
        :return: 返回数据
        """
        try:
            f = open(self.path, encoding='utf-8')
            data = yaml.load(f, Loader=yaml.FullLoader)
            f.close()
            return data
        except Exception as msg:
            print("异常消息-> {0}".format(msg))

    def get_id(self):
        """获取testInfo项的id元素"""
        data = self.get_yaml()
        return data['testInfo'][0]['id']

    def case_len(self):
        """
        testCase 字典长度
        :return: 字典长度大小
        """
        data = self.get_yaml()
        length = len(data['testCase'])
        return length

    def check_len(self):
        """
        check字典长度
        :return: 字典长度大小
        """
        data = self.get_yaml()
        length = len(data['check'])
        return length

    def get_element_info(self, i):
        """
        获取testCase项的element_info元素
        :param i: 位置序列号
        :return: 返回element_info元素数据
        """
        data = self.get_yaml()
        return data['testCase'][i]['element_info']

    def get_find_type(self, i):
        """
        获取testCase项的find_type元素数据
        :param i: 位置序列号
        :return: 返回find_type元素数据
        """
        data = self.get_yaml()
        return data['testCase'][i]['find_type']

    def get_operate_type(self, i):
        """
        获取testCase项的operate_type元素数据
        :param i: 位置序列号
        :return: 返回operate_type元素数据
        """
        data = self.get_yaml()
        return data['testCase'][i]['operate_type']

    def get_check_element_info(self, i):
        """
        获取check项的element_info元素
        :param i: 位置序列号
        :return: 返回element_info元素数据
        """
        data = self.get_yaml()
        return data['check'][i]['element_info']

    def get_check_find_type(self, i):
        """
        获取check项的find_type元素
        :param i: 位置序列号
        :return: 返回find_type元素数据
        """
        data = self.get_yaml()
        return data['check'][i]['find_type']

    def get_check_operate_type(self, i):
        """
        获取check项的operate_type元素
        :param i: 位置序列号
        :return: 返回operate_type元素数据
        """
        data = self.get_yaml()
        return data['check'][i]['operate_type']

    def get_check_info(self, i):
        """
        获取check项的info元素
        :param i: 位置序列号
        :return: 返回info元素数据
        """
        data = self.get_yaml()
        return data['check'][i]['info']

    def get_reuse_element_info(self, i):
        """
        获取reuse项的element_info元素
        :param i: 位置序列号
        :return: 返回element_info元素数据
        """
        data = self.get_yaml()
        return data['reuse'][i]['element_info']
