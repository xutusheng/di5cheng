# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/6
# @PROJECT : di5cheng-IT-PaaS
# @File    : test_service.py

import time
import random
from api import service, db_query
from common import random_param, config


class TestCase:

    def setup_class(self):
        self.ms = service.Service()
        self.db = db_query.DBQuery()
        # 登录
        login_result = self.ms.userlogin(a=int(config.get_account("service")["username"]),
                                         b=config.get_account("service")["password"])
        # 获取 user_id
        self.user_id = login_result["b"]
        user_info = self.ms.queryUserBasicInfo(user_id=self.user_id)
        # 获取企业id
        self.cpy_id = user_info["d"]["f"]

    def teardown_class(self):
        self.db.mysql.close()
        self.db.ssh.close()

    # 用例一：增加一个待审核车辆
    def test_case001(self):
        # 车牌号码
        car_number = random_param.Random_param().create_carNumber(5)
        # 车辆类型
        car_type = random.randint(1, 3)
        # 车辆识别代码
        car_code = random.randint(10000, 19999)
        # 许可证有效期
        car_Licence = (int(time.time()) + 200000) * 1000
        # 车辆七张图
        picture_list = [random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture())]
        add_result = self.ms.addCar(user_id=self.user_id, n=self.cpy_id, r=1, a=car_number, b=car_type, m=car_code,
                                    e=car_Licence, l=car_Licence, d=picture_list[0], f=picture_list[1],
                                    g=picture_list[2], h=picture_list[3], i=picture_list[4], j=picture_list[5],
                                    k=picture_list[6])
        assert add_result == {"a": "200"}
        # 查询车辆列表
        queryCarListInfo = self.ms.queryCarList(user_id=self.user_id, a=self.cpy_id, d=1, x=1, y=10)
        # 计数器count清零
        count = 0
        for car in queryCarListInfo["d"]:
            if car["e"] == car_number:
                count += 1
            else:
                continue
        assert count == 1

        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_carNum = self.db.querycarbycarnumber(car_number=car_number)
        cursor.execute(sql_carNum)
        car_data = cursor.fetchall()
        # 计数器count清零
        count = 0
        for car in car_data:
            car_num = car[4]
            if car_number == car_num:
                count += 1
        assert count == 1

    # 用例二：对比车辆列表数是否与数据库一致
    def test_case002(self):
        # 查询车辆列表
        queryCarListInfo = self.ms.queryCarList(user_id=self.user_id, a=self.cpy_id, d=1, x=1, y=10)
        CarList = queryCarListInfo["d"]
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_carlist = self.db.querydrivercarbycompany(company_id=self.cpy_id)
        cursor.execute(sql_carlist)
        car_list = cursor.fetchall()
        carlist = []
        for car in car_list:
            carlist.append(car)
            print(car)
        print(carlist)
        assert len(CarList) == len(carlist)

    # 用例三：修改一个待审核车辆信息(修改有效期)
    def test_case003(self):
        # 车牌号码
        car_number = random_param.Random_param().create_carNumber(5)
        # 车辆类型
        car_type = random.randint(1, 3)
        # 车辆识别代码
        car_code = str(random.randint(10000, 19999))
        # 车辆七张图
        picture_list = [random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture())]
        # 许可证有效期
        car_Licence = (int(time.time()) + 10000) * 1000
        add_result = self.ms.addCar(user_id=self.user_id, n=self.cpy_id, r=1, a=car_number, b=car_type, m=car_code,
                                    e=car_Licence, l=car_Licence, d=picture_list[0], f=picture_list[1],
                                    g=picture_list[2], h=picture_list[3], i=picture_list[4], j=picture_list[5],
                                    k=picture_list[6])
        assert add_result == {"a": "200"}
        # 查询车辆列表
        queryCarListInfo = self.ms.queryCarList(user_id=self.user_id, a=self.cpy_id, d=1, x=1, y=10)
        CarList = queryCarListInfo["d"]
        biz_id = 0
        car_LicenceEdit = 0
        for car in CarList:
            if car["e"] != car_number:
                continue
            else:
                # 修改后的有效期
                car_LicenceEdit = (int(time.time()) + 10000) * 1000
                biz_id = car["a"]
                edit_result = self.ms.carEdit(user_id=self.user_id, a=biz_id, u=self.cpy_id, b=car_type,
                                              c=picture_list[0], d=picture_list[1], e=picture_list[2],
                                              g=car_LicenceEdit, h=picture_list[3], i=picture_list[4],
                                              j=picture_list[5], k=picture_list[6], l=car_code, n=car_LicenceEdit,
                                              q=car["o"])
                assert edit_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_carcertlist = self.db.querycarcertinfobybizid(biz_id=biz_id)
        cursor.execute(sql_carcertlist)
        car_cert_data = cursor.fetchall()
        for car_cert in car_cert_data:
            if car_cert[2] == 2 or car_cert[2] == 3:
                continue
            else:
                assert int(car_cert[4]) == car_LicenceEdit
                assert int(car_cert[-1]) == self.user_id

    # 用例四：添加一个待审核挂车
    def test_case004(self):
        # 车牌号码
        gua_number = random_param.Random_param().create_carNumber(4)
        # 车辆类型
        gua_type = random.randint(1, 5)
        # 车辆识别代码
        gua_code = random.randint(10000, 19999)
        # 荷载吨数
        gua_ton = random.randint(10, 50) * 1000
        # 装口类型
        port_type = random.choice(['1', '2', "'1,2'"])
        # 许可证有效期
        gua_Licence = (int(time.time()) + 100000) * 1000
        # 车辆七张图
        picture_list = [random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture())]
        # 新增挂车
        add_result = self.ms.addguaCar(user_id=self.user_id, n=self.cpy_id, r=2, s=gua_number, c=gua_type,
                                       m=str(gua_code), e=gua_Licence, l=gua_Licence, p=gua_ton, q=port_type,
                                       d=picture_list[0], f=picture_list[1], g=picture_list[2], h=picture_list[3],
                                       i=picture_list[4], j=picture_list[5], k=picture_list[6])
        assert add_result == {"a": "200"}
        # 查询挂车列表
        queryCarListInfo = self.ms.queryCarList(user_id=self.user_id, a=self.cpy_id, d=2, x=1, y=10)
        # 计数器count清零
        count = 0
        for car in queryCarListInfo["d"]:
            if car["f"] == gua_number:
                count += 1
            else:
                continue
        assert count == 1

        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_guaNum = self.db.queryguacarbycarnumber(gua_number=gua_number)
        cursor.execute(sql_guaNum)
        gua_data = cursor.fetchall()
        # 计数器count清零
        count = 0
        for car in gua_data:
            print(car)
            gua_num = car[5]
            if gua_number == gua_num:
                count += 1
        assert count == 1

    # 用例五：修改一个待审核挂车信息(修改有效期)
    def test_case005(self):
        # 车牌号码
        car_number = random_param.Random_param().create_carNumber(4)
        # 车辆类型
        car_type = random.randint(1, 5)
        # 车辆识别代码
        car_code = random.randint(10000, 19999)
        # 荷载吨数
        car_ton = random.randint(10, 50) * 1000
        # 装口类型
        port_type = random.choice(['1', '2', "'1,2'"])
        # 许可证有效期
        car_Licence = (int(time.time()) + 300000) * 1000
        # 车辆七张图
        picture_list = [random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture())]
        # 新增挂车
        add_result = self.ms.addguaCar(user_id=self.user_id, n=self.cpy_id, r=2, s=car_number, c=car_type,
                                       m=str(car_code), e=car_Licence, l=car_Licence, p=car_ton, q=port_type,
                                       d=picture_list[0], f=picture_list[1], g=picture_list[2], h=picture_list[3],
                                       i=picture_list[4], j=picture_list[5], k=picture_list[6])
        assert add_result == {"a": "200"}
        # 查询挂车列表
        queryCarListInfo = self.ms.queryCarList(user_id=self.user_id, a=self.cpy_id, d=2, x=1, y=10)
        CarList = queryCarListInfo["d"]
        biz_id = 0
        car_LicenceEdit = 0
        for car in CarList:
            if car["f"] != car_number:
                continue
            else:
                # 修改后的有效期
                car_LicenceEdit = (int(time.time()) + 10000) * 1000
                biz_id = car["a"]
                edit_result = self.ms.guacarEdit(user_id=self.user_id, a=biz_id, u=self.cpy_id, b=car_type,
                                                 c=picture_list[0], d=picture_list[1], e=picture_list[2],
                                                 g=car_LicenceEdit, h=picture_list[3], i=picture_list[4],
                                                 j=picture_list[5], k=picture_list[6], l=car_code, n=car_LicenceEdit,
                                                 o=car_ton, p=port_type, q=car["o"])
                assert edit_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_carcertlist = self.db.querycarcertinfobybizid(biz_id=biz_id)
        cursor.execute(sql_carcertlist)
        car_cert_data = cursor.fetchall()
        for car_cert in car_cert_data:
            if car_cert[2] == 2 or car_cert[2] == 3:
                continue
            else:
                assert int(car_cert[4]) == car_LicenceEdit
                assert int(car_cert[-1]) == self.user_id

    # 添加一个司机并修改有效期
    def test_case006(self):
        # 司机姓名
        driver_name = random_param.Random_param().create_name()
        # 司机手机号码
        driver_phone = int(random_param.Random_param().create_Phone())
        # 司机身份证号码
        driver_IDcard = random_param.Random_param().create_IDcard()
        # 从业资格证号码
        certificate_number = int(time.time())
        # 有效期
        driver_Licence = (int(time.time()) + 300000) * 1000
        # 三张照片
        picture_list = [random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture())]
        # 添加一个司机
        add_result = self.ms.addDriver(user_id=self.user_id, a=self.cpy_id, b=driver_name, c=driver_IDcard,
                                       d=driver_phone, e=picture_list[0], f=picture_list[1], h=picture_list[2],
                                       j=certificate_number, g=driver_Licence, i=driver_Licence, m=1)
        assert add_result == {"a": "200"}
        # 司机列表中查询司机
        driverListinfo = self.ms.querydriverList(user_id=self.user_id, a=self.cpy_id, d=1, x=1, y=10)
        driverList = driverListinfo["d"]
        # 计数器清零
        count = 0
        driver_no = 0
        driver_user_id = 0
        for driver in driverList:
            if driver["b"] == driver_phone:
                count += 1
                driver_no = driver["c"]
                driver_user_id = driver["h"]
            else:
                continue
        assert count == 1
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_driverlist = self.db.querydriverinfobyid(id=driver_no, type=1)
        cursor.execute(sql_driverlist)
        driverlist_data = cursor.fetchall()
        for data in driverlist_data:
            assert int(data[1]) == driver_user_id
        # 修改后的有效期
        driver_Licence_new = (int(time.time()) + 300000) * 1000
        # 修改司机信息
        modify_result = self.ms.modifyDriver(user_id=self.user_id, a=self.cpy_id, b=driver_name, c=driver_IDcard,
                                             d=driver_phone, e=picture_list[0], f=picture_list[1], h=picture_list[2],
                                             j=certificate_number, g=driver_Licence_new, i=driver_Licence_new, m=1)
        assert modify_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_driverlist = self.db.querydrivercertinfobyid(biz_id=driver_no)
        cursor.execute(sql_driverlist)
        driverlist_data = cursor.fetchall()
        for data in driverlist_data:
            assert int(data[4]) == driver_Licence_new

    # 添加一个押运员并修改有效期
    def test_case007(self):
        # 押运员姓名
        ya_driver_name = random_param.Random_param().create_name()
        # 押运员手机号
        ya_driver_phone = int(random_param.Random_param().create_Phone())
        # 有效期
        driver_Licence = (int(time.time()) + 300000) * 1000
        # 照片
        picture = random.choice(config.get_picture())
        # 添加一个押运员
        add_result = self.ms.addyaDriver(user_id=self.user_id, a=self.cpy_id, b=ya_driver_name, d=ya_driver_phone,
                                         k=picture, l=driver_Licence, m=2)
        assert add_result == {"a": "200"}
        # 押运员列表中查询押运员
        driverListinfo = self.ms.querydriverList(user_id=self.user_id, a=self.cpy_id, d=2, x=1, y=10)
        driverList = driverListinfo["d"]
        # 计数器清零
        count = 0
        driver_no = 0
        for driver in driverList:
            if driver["b"] == ya_driver_phone:
                count += 1
                driver_no = driver["a"]
            else:
                continue
        assert count == 1
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_driverlist = self.db.querydriverinfobyid(id=driver_no, type=1)
        cursor.execute(sql_driverlist)
        driverlist_data = cursor.fetchall()
        for data in driverlist_data:
            assert int(data[4]) == ya_driver_phone
        # 修改后的有效期
        driver_Licence_new = (int(time.time()) + 300000) * 1000
        # 修改司机信息
        modify_result = self.ms.modifyEscort(user_id=self.user_id, a=self.cpy_id, b=ya_driver_name, d=ya_driver_phone,
                                             k=picture, l=driver_Licence_new, m=2)
        assert modify_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_driverlist = self.db.querydrivercertinfobyid(biz_id=driver_no)
        cursor.execute(sql_driverlist)
        driverlist_data = cursor.fetchall()
        for data in driverlist_data:
            assert int(data[4]) == driver_Licence_new

    # 添加一个运力（车、司机）
    def test_case008(self):
        # 车牌号码
        car_number = random_param.Random_param().create_carNumber(5)
        # 车辆类型
        car_type = random.randint(1, 3)
        # 车辆识别代码
        car_code = random.randint(10000, 19999)
        # 许可证有效期
        car_Licence = (int(time.time()) + 200000) * 1000
        # 车辆七张图
        picture_list = [random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture())]
        add_result = self.ms.addCar(user_id=self.user_id, n=self.cpy_id, r=1, a=car_number, b=car_type, m=car_code,
                                    e=car_Licence, l=car_Licence, d=picture_list[0], f=picture_list[1],
                                    g=picture_list[2], h=picture_list[3], i=picture_list[4], j=picture_list[5],
                                    k=picture_list[6])
        assert add_result == {"a": "200"}
        # 司机姓名
        driver_name = random_param.Random_param().create_name()
        # 司机手机号码
        driver_phone = int(random_param.Random_param().create_Phone())
        # 司机身份证号码
        driver_IDcard = random_param.Random_param().create_IDcard()
        # 从业资格证号码
        certificate_number = int(time.time())
        # 有效期
        driver_Licence = (int(time.time()) + 300000) * 1000
        # 三张照片
        picture_list = [random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture())]
        # 添加一个司机
        add_result = self.ms.addDriver(user_id=self.user_id, a=self.cpy_id, b=driver_name, c=driver_IDcard,
                                       d=driver_phone, e=picture_list[0], f=picture_list[1], h=picture_list[2],
                                       j=certificate_number, g=driver_Licence, i=driver_Licence, m=1)
        assert add_result == {"a": "200"}
        # 查询 车辆id
        query_carlist = self.ms.carQueryList(user_id=self.user_id, a=self.cpy_id, b=car_number)
        car_id = query_carlist["d"][0]["b"]
        # 查询 司机id ，uid
        query_driverlist = self.ms.driverQueryList(user_id=self.user_id, a=self.cpy_id, b=driver_name)
        driver_id = query_driverlist["d"][0]["b"]
        driver_uid = query_driverlist["d"][0]["c"]
        # 添加运力
        add_result = self.ms.addTransport(user_id=self.user_id, a=self.cpy_id, b=car_id, d=driver_id, e=driver_uid)
        assert add_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_transport = self.db.querytransportinfobyid(company_id=self.cpy_id)
        cursor.execute(sql_transport)
        transport_data = cursor.fetchall()
        # 计数器count清零
        count = 0
        for transport in transport_data:
            print(transport)
            carid = transport[2]
            driverid = transport[4]
            driveruid = transport[5]
            if carid == car_id and driverid == driver_id and driveruid == driver_uid:
                count += 1
            else:
                continue
        assert count == 1

    # 添加一个运力（车、挂车、司机、押运员）\并修改挂车
    def test_case009(self):
        # 车牌号码
        car_number = random_param.Random_param().create_carNumber(5)
        # 车辆类型
        car_type = random.randint(1, 3)
        # 车辆识别代码
        car_code = random.randint(10000, 19999)
        # 许可证有效期
        car_Licence = (int(time.time()) + 200000) * 1000
        # 车辆七张图
        picture_list = [random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture())]
        # 新增车辆
        add_result = self.ms.addCar(user_id=self.user_id, n=self.cpy_id, r=1, a=car_number, b=car_type, m=car_code,
                                    e=car_Licence, l=car_Licence, d=picture_list[0], f=picture_list[1],
                                    g=picture_list[2], h=picture_list[3], i=picture_list[4], j=picture_list[5],
                                    k=picture_list[6])
        assert add_result == {"a": "200"}
        # 车牌号码
        gua_number = random_param.Random_param().create_carNumber(4)
        # 车辆类型
        gua_type = random.randint(1, 5)
        # 车辆识别代码
        gua_code = random.randint(10000, 19999)
        # 荷载吨数
        gua_ton = random.randint(10, 50) * 1000
        # 装口类型
        port_type = random.choice(['1', '2', "'1,2'"])
        # 许可证有效期
        gua_Licence = (int(time.time()) + 100000) * 1000
        # 车辆七张图
        picture_list = [random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture())]
        # 新增挂车
        add_result = self.ms.addguaCar(user_id=self.user_id, n=self.cpy_id, r=2, s=gua_number, c=gua_type,
                                       m=str(gua_code), e=gua_Licence, l=gua_Licence, p=gua_ton, q=port_type,
                                       d=picture_list[0], f=picture_list[1], g=picture_list[2], h=picture_list[3],
                                       i=picture_list[4], j=picture_list[5], k=picture_list[6])
        assert add_result == {"a": "200"}
        # 司机姓名
        driver_name = random_param.Random_param().create_name()
        # 司机手机号码
        driver_phone = int(random_param.Random_param().create_Phone())
        # 司机身份证号码
        driver_IDcard = random_param.Random_param().create_IDcard()
        # 从业资格证号码
        certificate_number = int(time.time())
        # 有效期
        driver_Licence = (int(time.time()) + 300000) * 1000
        # 三张照片
        picture_list = [random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture())]
        # 添加一个司机
        add_result = self.ms.addDriver(user_id=self.user_id, a=self.cpy_id, b=driver_name, c=driver_IDcard,
                                       d=driver_phone, e=picture_list[0], f=picture_list[1], h=picture_list[2],
                                       j=certificate_number, g=driver_Licence, i=driver_Licence, m=1)
        assert add_result == {"a": "200"}
        # 押运员姓名
        ya_driver_name = random_param.Random_param().create_name()
        # 押运员手机号
        ya_driver_phone = int(random_param.Random_param().create_Phone())
        # 有效期
        driver_Licence = (int(time.time()) + 300000) * 1000
        # 照片
        picture = random.choice(config.get_picture())
        # 添加一个押运员
        add_result = self.ms.addyaDriver(user_id=self.user_id, a=self.cpy_id, b=ya_driver_name, d=ya_driver_phone,
                                         k=picture, l=driver_Licence, m=2)
        assert add_result == {"a": "200"}
        # 查询 车辆id
        query_carlist = self.ms.carQueryList(user_id=self.user_id, a=self.cpy_id, b=car_number)
        car_id = query_carlist["d"][0]["b"]
        # 查询 挂车id
        query_gualist = self.ms.guaQueryList(user_id=self.user_id, a=self.cpy_id, b=gua_number)
        gua_id = query_gualist["d"][0]["b"]
        # 查询 司机id ，uid
        query_driverlist = self.ms.driverQueryList(user_id=self.user_id, a=self.cpy_id, b=driver_name)
        driver_id = query_driverlist["d"][0]["b"]
        driver_uid = query_driverlist["d"][0]["c"]
        # 查询 押运员id ，uid
        query_yadriverlist = self.ms.escortQueryList(user_id=self.user_id, a=self.cpy_id, b=ya_driver_name)
        ya_driver_id = query_yadriverlist["d"][0]["b"]
        # 添加运力
        add_result = self.ms.addTransport(user_id=self.user_id, a=self.cpy_id, b=car_id, d=driver_id, e=driver_uid,
                                          c=gua_id, f=ya_driver_id, g="")
        assert add_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_transport = self.db.querytransportinfobyid(company_id=self.cpy_id)
        cursor.execute(sql_transport)
        transport_data = cursor.fetchall()
        # 计数器count清零
        count = 0
        for transport in transport_data:
            print(transport)
            carid = transport[2]
            guaid = transport[3]
            driverid = transport[4]
            driveruid = transport[5]
            escortid = transport[6]
            if carid == car_id and guaid == gua_id and driverid == driver_id and driveruid == driver_uid and \
                    escortid == ya_driver_id:
                count += 1
            else:
                continue
        assert count == 1

        # 修改挂车信息
        add_result = self.ms.editTransport(user_id=self.user_id, a=self.cpy_id, b=car_id, d=driver_id, e=driver_uid,
                                           c="", f=ya_driver_id, g="")
        assert add_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_transport = self.db.querytransportinfobyid(company_id=self.cpy_id)
        cursor.execute(sql_transport)
        transport_data = cursor.fetchall()
        # 计数器count清零
        count = 0
        for transport in transport_data:
            print(transport)
            carid = transport[2]
            guaid = transport[3]
            driverid = transport[4]
            driveruid = transport[5]
            escortid = transport[6]
            if carid == car_id and guaid is None and driverid == driver_id and driveruid == driver_uid and \
                    escortid == ya_driver_id:
                count += 1
            else:
                continue
        assert count == 1

    # 删除一个运力
    def test_case010(self):
        # 车牌号码
        car_number = random_param.Random_param().create_carNumber(5)
        # 车辆类型
        car_type = random.randint(1, 3)
        # 车辆识别代码
        car_code = random.randint(10000, 19999)
        # 许可证有效期
        car_Licence = (int(time.time()) + 200000) * 1000
        # 车辆七张图
        picture_list = [random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture())]
        add_result = self.ms.addCar(user_id=self.user_id, n=self.cpy_id, r=1, a=car_number, b=car_type, m=car_code,
                                    e=car_Licence, l=car_Licence, d=picture_list[0], f=picture_list[1],
                                    g=picture_list[2], h=picture_list[3], i=picture_list[4], j=picture_list[5],
                                    k=picture_list[6])
        assert add_result == {"a": "200"}
        # 司机姓名
        driver_name = random_param.Random_param().create_name()
        # 司机手机号码
        driver_phone = int(random_param.Random_param().create_Phone())
        # 司机身份证号码
        driver_IDcard = random_param.Random_param().create_IDcard()
        # 从业资格证号码
        certificate_number = int(time.time())
        # 有效期
        driver_Licence = (int(time.time()) + 300000) * 1000
        # 三张照片
        picture_list = [random.choice(config.get_picture()),
                        random.choice(config.get_picture()),
                        random.choice(config.get_picture())]
        # 添加一个司机
        add_result = self.ms.addDriver(user_id=self.user_id, a=self.cpy_id, b=driver_name, c=driver_IDcard,
                                       d=driver_phone, e=picture_list[0], f=picture_list[1], h=picture_list[2],
                                       j=certificate_number, g=driver_Licence, i=driver_Licence, m=1)
        assert add_result == {"a": "200"}
        # 查询 车辆id
        query_carlist = self.ms.carQueryList(user_id=self.user_id, a=self.cpy_id, b=car_number)
        car_id = query_carlist["d"][0]["b"]
        # 查询 司机id ，uid
        query_driverlist = self.ms.driverQueryList(user_id=self.user_id, a=self.cpy_id, b=driver_name)
        driver_id = query_driverlist["d"][0]["b"]
        driver_uid = query_driverlist["d"][0]["c"]
        # 添加运力
        add_result = self.ms.addTransport(user_id=self.user_id, a=self.cpy_id, b=car_id, d=driver_id, e=driver_uid)
        assert add_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_transport = self.db.querytransportinfobyid(company_id=self.cpy_id)
        cursor.execute(sql_transport)
        transport_data = cursor.fetchall()
        # 计数器count清零
        count = 0
        transport_id = 0
        for transport in transport_data:
            print(transport)
            transport_id = transport[0]
            carid = transport[2]
            driverid = transport[4]
            driveruid = transport[5]
            if carid == car_id and driverid == driver_id and driveruid == driver_uid:
                count += 1
            else:
                continue
        assert count == 1
        # 删除这个运力
        del_result = self.ms.delTransport(user_id=self.user_id, a=transport_id)
        assert del_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_transport = self.db.querytransportinfobyid(company_id=self.cpy_id)
        cursor.execute(sql_transport)
        transport_data = cursor.fetchall()
        # 计数器count清零
        count = 0
        for transport in transport_data:
            print(transport)
            carid = transport[2]
            driverid = transport[4]
            driveruid = transport[5]
            if carid == car_id and driverid == driver_id and driveruid == driver_uid:
                count += 1
            else:
                continue
        assert count == 0

    # 添加-修改-删除常用装货地址
    def test_case011(self):
        # 客服登录
        login_result = self.ms.userlogin(a=13382017556, b="123456")
        # 获取 user_id
        user_id = login_result["b"]
        # 随机一个三级联动地址
        address = random_param.Random_param().create_area_name()
        # 随机一个详细地址
        full_address = "团结路" + str(int(time.time())) + "号"
        # 添加一个常用装货地址
        add_result = self.ms.addressAddOrUpdate(user_id=user_id, b=user_id, c=address, d=full_address, e=1, g=1)
        assert add_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_addressinfo = self.db.queryaddressinfobyuserid(user_id=user_id, address_sort=1)
        cursor.execute(sql_addressinfo)
        addressinfo_data = cursor.fetchall()
        # 计数器count清零
        count = 0
        for addressinfo in addressinfo_data:
            print(addressinfo)
            three_linkage = addressinfo[2]
            detailed_address = addressinfo[3]
            if three_linkage == address and full_address == detailed_address:
                count += 1
            else:
                continue
        assert count == 1
        # 查列表
        address_list = self.ms.addressFind(user_id=user_id, a=user_id, b=1, c=1, d=10)
        # 计数器count清零
        count = 0
        add_id = 0
        for add_info in address_list["d"]:
            if add_info["b"] == address and add_info["c"] == full_address:
                count += 1
                add_id = add_info["a"]
            else:
                continue
        assert count == 1
        # 修改地址
        full_address_new = "团结路" + str(int(time.time())) + "号"
        add_result = self.ms.addressAddOrUpdate(user_id=user_id, a=add_id, b=user_id, c=address, d=full_address_new,
                                                e=1, g=1)
        assert add_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_addressinfo = self.db.queryaddressinfobyuserid(user_id=user_id, address_sort=1)
        cursor.execute(sql_addressinfo)
        addressinfo_data = cursor.fetchall()
        # 计数器count清零
        count = 0
        for addressinfo in addressinfo_data:
            print(addressinfo)
            three_linkage = addressinfo[2]
            detailed_address = addressinfo[3]
            if three_linkage == address and full_address_new == detailed_address:
                count += 1
            else:
                continue
        assert count == 1
        # 删除 地址
        del_result = self.ms.addressDelete(user_id=user_id, a=add_id)
        assert del_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_addressinfo = self.db.queryaddressinfobyuserid(user_id=user_id, address_sort=1)
        cursor.execute(sql_addressinfo)
        addressinfo_data = cursor.fetchall()
        # 计数器count清零
        count = 0
        for addressinfo in addressinfo_data:
            print(addressinfo)
            three_linkage = addressinfo[2]
            detailed_address = addressinfo[3]
            if three_linkage == address and full_address == detailed_address:
                count += 1
            else:
                continue
        assert count == 0
        # 查列表
        address_list = self.ms.addressFind(user_id=user_id, a=user_id, b=1, c=1, d=10)
        # 计数器count清零
        count = 0
        for add_info in address_list["d"]:
            if add_info["b"] == address and add_info["c"] == full_address:
                count += 1
            else:
                continue
        assert count == 0

    # 添加-修改-删除常用卸货地址
    def test_case012(self):
        # 客服登录
        login_result = self.ms.userlogin(a=13382017556, b="123456")
        # 获取 user_id
        user_id = login_result["b"]
        # 随机一个三级联动地址
        address = random_param.Random_param().create_area_name()
        # 随机一个详细地址
        full_address = "团结路" + str(int(time.time())) + "号"
        # 添加一个常用卸货地址
        add_result = self.ms.addressAddOrUpdate(user_id=user_id, b=user_id, c=address, d=full_address, e=2, g=1)
        assert add_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_addressinfo = self.db.queryaddressinfobyuserid(user_id=user_id, address_sort=2)
        cursor.execute(sql_addressinfo)
        addressinfo_data = cursor.fetchall()
        # 计数器count清零
        count = 0
        for addressinfo in addressinfo_data:
            print(addressinfo)
            three_linkage = addressinfo[2]
            detailed_address = addressinfo[3]
            if three_linkage == address and full_address == detailed_address:
                count += 1
            else:
                continue
        assert count == 1
        # 查列表
        address_list = self.ms.addressFind(user_id=user_id, a=user_id, b=2, c=1, d=10)
        # 计数器count清零
        count = 0
        add_id = 0
        for add_info in address_list["d"]:
            if add_info["b"] == address and add_info["c"] == full_address:
                count += 1
                add_id = add_info["a"]
            else:
                continue
        assert count == 1
        # 修改地址
        full_address_new = "团结路" + str(int(time.time())) + "号"
        add_result = self.ms.addressAddOrUpdate(user_id=user_id, a=add_id, b=user_id, c=address, d=full_address_new,
                                                e=2, g=1)
        assert add_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_addressinfo = self.db.queryaddressinfobyuserid(user_id=user_id, address_sort=2)
        cursor.execute(sql_addressinfo)
        addressinfo_data = cursor.fetchall()
        # 计数器count清零
        count = 0
        for addressinfo in addressinfo_data:
            print(addressinfo)
            three_linkage = addressinfo[2]
            detailed_address = addressinfo[3]
            if three_linkage == address and full_address_new == detailed_address:
                count += 1
            else:
                continue
        assert count == 1
        # 删除 地址
        del_result = self.ms.addressDelete(user_id=user_id, a=add_id)
        assert del_result == {"a": "200"}
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_addressinfo = self.db.queryaddressinfobyuserid(user_id=user_id, address_sort=2)
        cursor.execute(sql_addressinfo)
        addressinfo_data = cursor.fetchall()
        # 计数器count清零
        count = 0
        for addressinfo in addressinfo_data:
            print(addressinfo)
            three_linkage = addressinfo[2]
            detailed_address = addressinfo[3]
            if three_linkage == address and full_address == detailed_address:
                count += 1
            else:
                continue
        assert count == 0
        # 查列表
        address_list = self.ms.addressFind(user_id=user_id, a=user_id, b=2, c=1, d=10)
        # 计数器count清零
        count = 0
        for add_info in address_list["d"]:
            if add_info["b"] == address and add_info["c"] == full_address:
                count += 1
            else:
                continue
        assert count == 0

    # 发布货单
    def test_case013(self):
        # 客服登录
        login_result = self.ms.userlogin(a=19900000001, b="123456")
        # 获取 user_id
        user_id = login_result["b"]
        # 查询参数字典
        dictionaries = self.ms.dictionaries(user_id=user_id)
        # 装货地
        loading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
        # 卸货地
        unloading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
        # 货品名称
        used_product_name_list = self.ms.msDsFind(user_id=user_id)
        if used_product_name_list["d"] == []:
            product_name = random.choice(["甲苯", "二甲苯", "MTBE", "石脑油", "减水剂"])
        else:
            product_name = random.choice(used_product_name_list["d"])["b"]
        # 货品单价
        per_price = random.randint(1000, 2000) * 100
        # 装货时间
        loading_time = (int(time.time()) + 200000) * 1000
        # 需求车数
        need_car_num = random.randint(10, 20)
        # 发货数值单位
        unit_type = random.choice(dictionaries["d"][5]["b"])["b"]
        # 发货数值
        if unit_type == 1:
            unit = random.randint(500, 1000) * 1000
        else:
            unit = random.randint(500, 1000)
        # 发货类型
        invoice_type = random.randint(1, 2)
        # 随机一个三级联动地址
        up_address = random_param.Random_param().create_area_name()
        # 随机一个详细地址
        full_up_address = "团结路" + str(int(time.time())) + "号"
        # 添加一个常用卸货地址
        add_result = self.ms.addressAddOrUpdate(user_id=user_id, b=user_id, c=up_address, d=full_up_address, e=1, g=1)
        assert add_result == {"a": "200"}
        # 随机一个三级联动地址
        down_address = random_param.Random_param().create_area_name()
        # 随机一个详细地址
        full_down_address = "胜利路" + str(int(time.time()) + 100) + "号"
        # 添加一个常用卸货地址
        add_result = self.ms.addressAddOrUpdate(user_id=user_id, b=user_id, c=down_address, d=full_down_address, e=2,
                                                g=1)
        assert add_result == {"a": "200"}
        # 损耗值单位
        down_type = random.choice(dictionaries["d"][4]["b"])["b"]
        # 损耗值
        if down_type == 1:
            down = random.randint(0, 5)
        else:
            down = random.randint(10, 500)
        # 运单、车队指导价
        down_pirce = random.randint(500, 700) * 100
        # 查询货主
        company_list = self.ms.companyFind(user_id=user_id)
        # 选择一个货主
        company_info = random.choice(company_list["d"])
        company_id = company_info["a"]
        company_name = company_info["b"]
        # 上家价格
        up_price = random.randint(700, 1000) * 100
        # 开票
        billing_type = random.choice([0, 1])
        # 查询小五
        dispatch_list = self.ms.x5List(user_id=user_id)
        dispatch_info = random.choice(dispatch_list["d"])
        dispatch_id = dispatch_info["a"]
        dispatch_name = dispatch_info["b"]
        # 选择小五
        dispatches = [{"a": dispatch_id, "b": dispatch_name}]
        # 备注
        remark = "auto test"
        # 备注 2
        remark2 = random.choice(["卸结", "好装好卸", "干净货", "蒸罐", "要报备车", "下装口", "车数可循环"])
        # 账期
        return_type = random.choice(dictionaries["d"][1]["b"])["b"]
        # 账期值
        return_value = random.randint(700, 1000) * 100
        # 结算方式
        settle_type = random.choice(dictionaries["d"][0]["b"])["b"]
        # 结算值
        settle = random.randint(700, 1000) * 100
        # 付款方式
        pay_type = random.choice(dictionaries["d"][2]["b"])["b"]
        # 付款值
        pay = random.randint(700, 1000) * 100
        # 计费方式
        price_type = random.choice(dictionaries["d"][3]["b"])["b"]
        # 核算磅单
        pounds_type = random.choice(dictionaries["d"][6]["b"])["b"]
        # 是否包含税点
        point = random.choice([0, 1])

        add_result = self.ms.fixedAdd(user_id=user_id, a=invoice_type, aa=return_value, ab=settle_type, ac=pay_type,
                                      ad=price_type, ae=1, af=loading_time, ag=remark2, ah=return_type, ai=unit_type,
                                      aj=pounds_type, ak=settle, al=pay, b=company_id, c=up_address, d=down_address,
                                      e=product_name, f=loading_s, g=unit, h=need_car_num, i=down, j=unloading_s,
                                      k=up_price, l=billing_type, m=down_pirce, n=point, o=per_price, p=remark,
                                      q=dispatches, r=down_type, s=full_up_address, t=full_down_address, u=company_name,
                                      v=1)
        assert add_result["a"] == "200"
        source_id = add_result["d"]["b"]
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_goodsinfo = self.db.querygoodsorderinfobyorderid(g_serial=source_id)
        cursor.execute(sql_goodsinfo)
        goodsinfo = cursor.fetchone()
        print(goodsinfo)
        assert goodsinfo[3] == product_name
        assert goodsinfo[4] == up_address
        assert goodsinfo[5] == full_up_address
        # 查列表
        count = 0
        goodslist = self.ms.listPaging(user_id=user_id, x=1, y=10)
        for goods in goodslist["d"]:
            if goods["x"] == source_id:
                count += 1
            else:
                continue
        assert count == 1

    # 发布询价
    def test_case014(self):
        # 客服登录
        login_result = self.ms.userlogin(a=13382017556, b="123456")
        # 获取 user_id
        user_id = login_result["b"]
        # 查询参数字典
        dictionaries = self.ms.dictionaries(user_id=user_id)
        # 装货地
        loading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
        # 卸货地
        unloading_s = random.choice(["广州 深圳", "上海 黄埔", "江苏 南京", "安徽 滁州", "山东 东营"])
        # 货品名称
        used_product_name_list = self.ms.msDsFind(user_id=user_id)
        if used_product_name_list["d"] == []:
            product_name = random.choice(["甲苯", "二甲苯", "MTBE", "石脑油", "减水剂"])
        else:
            product_name = random.choice(used_product_name_list["d"])["b"]
        # 装货时间
        loading_time = (int(time.time()) + 200000) * 1000
        # 需求车数
        need_car_num = random.randint(10, 20)
        # 发货数值单位
        unit_type = random.choice(dictionaries["d"][5]["b"])["b"]
        # 发货数值
        if unit_type == 1:
            unit = random.randint(500, 1000) * 1000
        else:
            unit = random.randint(500, 1000)
        # 发货类型
        invoice_type = random.randint(1, 2)
        # 开票
        billing_type = random.choice([0, 1])
        # 查询小五
        dispatch_list = self.ms.x5List(user_id=user_id)
        dispatch_info = random.choice(dispatch_list["d"])
        dispatch_id = dispatch_info["a"]
        dispatch_name = dispatch_info["b"]
        # 选择小五
        dispatches = [{"a": dispatch_id, "b": dispatch_name}]
        # 备注
        remark = "auto test"
        # 账期
        return_type = random.choice(dictionaries["d"][1]["b"])["b"]
        # 账期值
        return_value = random.randint(700, 1000) * 100
        add_result = self.ms.inquiryAdd(user_id=user_id, a=invoice_type, b=need_car_num, c=loading_s, d=unloading_s,
                                        e=product_name, f=loading_time, g=unit, h=billing_type, i=return_type,
                                        j=dispatches, n=1, o=unit_type, k=remark, m=return_value)
        assert add_result["a"] == "200"
        inquiry_id = add_result["d"]["b"]
        # 查询数据库
        cursor = self.db.mysql.cursor()
        sql_inquiryinfo = self.db.queryinquiryinfobyorderid(inquiry_no=inquiry_id)
        cursor.execute(sql_inquiryinfo)
        inquiryinfo = cursor.fetchone()
        print(inquiryinfo)
        assert inquiryinfo[5] == inquiry_id
        assert inquiryinfo[6] == loading_s
        assert inquiryinfo[7] == unloading_s
        # 查列表
        count = 0
        inquirylist = self.ms.inquiryManageList(user_id=user_id, f=1, g=10, h=0)
        for inquiry in inquirylist["d"]:
            if inquiry["f"] == inquiry_id:
                count += 1
            else:
                continue
        assert count == 1
