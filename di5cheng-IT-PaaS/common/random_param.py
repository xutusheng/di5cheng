# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/17
# @PROJECT : di5cheng-IT-MSS
# @File    : random_param.py

import faker
import re
import xlrd
import random
import datetime
from common import config

areaCode = r'地区编码'
car_area = r'车牌区号'
user_name = r'姓名'
area_dict = r'全国地区编码'

# 获取excel文件
workbook = xlrd.open_workbook(config.get_excel())

# 获取车牌区号
sheet_car = workbook.sheet_by_name(car_area)
prelist_car = sheet_car.col_values(0)

# 获取地区编码
sheet_area = workbook.sheet_by_name(areaCode)
prelist_area = sheet_area.col_values(1)

# 获取姓名
sheet_name = workbook.sheet_by_name(user_name)
first_name = sheet_name.col_values(0)
second_name = sheet_name.col_values(1)

# 获取全国地区编码
sheet_area_dict = workbook.sheet_by_name(area_dict)
sheet_area_dict_nrows = sheet_area_dict.nrows

# 获取图片id
pic = random.choice(config.get_picture())


class Random_param:

    def __init__(self):
        self.f = faker.Faker(locale='zh-CN')

    # 获取详细地址
    def get_detailed_address(self):
        addr = self.f.address()
        search_obj = re.search(r'(.+) ', addr)
        return search_obj.group(1)

    def random_num(self, num):
        ret = ""
        for i in range(num):
            num1 = random.randint(0, 9)
            s = str(random.choice([num1]))
            ret += s
        return ret

    # 随机车牌区号
    def car_areaCode(self):
        a = ""
        while a == "":
            a = random.choice(prelist_car)
        return a

    '''
    排列顺序从左至右依次为：六位数字地址码，八位数字出生日期码，三位数字顺序码和一位校验码:
    1、地址码 
    表示编码对象常住户口所在县(市、旗、区)的行政区域划分代码，按GB/T2260的规定执行。
    2、出生日期码 
    表示编码对象出生的年、月、日，按GB/T7408的规定执行，年、月、日代码之间不用分隔符。 
    3、顺序码 
    表示在同一地址码所标识的区域范围内，对同年、同月、同日出生的人编定的顺序号，顺序码的奇数分配给男性，偶数分配给女性。 
    4、校验码计算步骤
        (1)十七位数字本体码加权求和公式 
        S = Sum(Ai * Wi), i = 0, ... , 16 ，先对前17位数字的权求和 
        Ai:表示第i位置上的身份证号码数字值(0~9) 
        Wi:7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2 （表示第i位置上的加权因子）
        (2)计算模 
        Y = mod(S, 11)
        (3)根据模，查找得到对应的校验码 
        Y: 0 1 2 3 4 5 6 7 8 9 10 
        校验码: 1 0 X 9 8 7 6 5 4 3 2
    '''

    def getCheckBit(self, num17):
        """
        获取身份证最后一位，即校验码
        :param num17: 身份证前17位字符串
        :return: 身份证最后一位
        """
        Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        checkCode = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        zipWiNum17 = zip(list(num17), Wi)
        S = sum(int(i) * j for i, j in zipWiNum17)
        Y = S % 11
        return checkCode[Y]

    def getAddrCode(self):
        """
        获取身份证前6位，即地址码
        :return: 身份证前6位
        """
        addrIndex = random.choice(prelist_area)
        return addrIndex

    def getBirthday(self, start="1900-01-01", end="2018-12-30"):
        """
        获取身份证7到14位，即出生年月日
        :param start: 出生日期合理的起始时间
        :param end: 出生日期合理的结束时间
        :return: 份证7到14位
        """
        days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
        birthday = datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days))
        return datetime.datetime.strftime(birthday, "%Y%m%d")

    def create_IDcard(self, sex=1):
        """
        获取随机身份证
        :param sex: 性别，默认为男
        :return: 返回一个随机身份证
        """
        idNumber = int(self.getAddrCode())
        idCode = str(idNumber) + self.getBirthday()
        for i in range(2):
            idCode += str(random.randint(0, 9))
        idCode += str(random.randrange(sex, 9, 2))
        idCode += self.getCheckBit(idCode)
        return idCode

    # 生成随机2-3位姓名
    def create_name(self):
        a = ""
        while a == "":
            a = random.choice(first_name)
        b = ""
        while b == "":
            b = random.choice(second_name)
        full_name = a + "".join(b for i in range(random.randint(1, 2)))
        return full_name

    # 生成随机手机号
    def create_Phone(self):
        a = str(random.randint(130, 199)) + "".join(random.choice("0123456789") for i in range(8))
        return a

    # 生成随机车牌号
    def create_carNumber(self, length):
        area_code = self.car_areaCode()
        length_num = self.random_num(length)
        if length == 4:
            car_num = area_code + length_num + "挂"
        else:
            car_num = area_code + length_num
        return car_num

    # 生成随机省市区
    def create_area_name(self):
        name = ""
        for n in range(1, sheet_area_dict_nrows):
            area_dict_info = sheet_area_dict.row_values(random.randint(1, sheet_area_dict_nrows - 1))
            if int(area_dict_info[4]) == 3:
                area_name = area_dict_info[7]
                m = area_name.split(',')
                name = m[1] + "-" + m[2] + "-" + m[3]
                break
            else:
                continue
        return name

    # 获取缩写地址
    def get_abbr_address(self):
        name = ""
        for n in range(1, sheet_area_dict_nrows):
            area_dict_info = sheet_area_dict.row_values(random.randint(1, sheet_area_dict_nrows - 1))
            if int(area_dict_info[4]) == 3:
                area_name = area_dict_info[7]
                m = area_name.split(',')
                name = m[2]
                break
            else:
                continue
        return name

    # 获取姓名
    def get_name(self):
        return self.f.name()

    # 获取手机号
    def get_phone(self):
        return self.f.phone_number()

    # 获取公司名称
    def get_company(self):
        return self.f.company()


if __name__ == '__main__':
    r = Random_param()
    print(r.get_name())
    print(r.get_phone())
    print(r.get_company())
    print(r.create_IDcard())
    print(r.get_detailed_address())
    print(type(r.get_phone()))
