# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/17
# @PROJECT : di5cheng-IT-PaaS
# @File    : test_web.py

import random
from api import web, db_query
from common import random_param, provide_data, ParseWord, config
from common.logger import MyLog

null = None


class TestCase:

    global null

    def setup_class(self):
        self.url = config.get_url()
        self.log = MyLog().logger()
        self.rand = random_param.Random_param()
        self.word = ParseWord.ParseWord(config.get_word())
        self.web = web.Web()
        self.db = db_query.DBQuery()

        # 客服登录
        self.service_login_result = self.web.user_login_web(19900000001, '123456')
        # 车队登录
        self.fleet_login_result = self.web.user_login_web(19933334444, '123456')
        self.fleet_id = self.web.get_user_info(*self.fleet_login_result)
        # 管理员登录
        self.admin_user_id = self.web.user_login_web(19999999999, '123456')

    def teardown_class(self):
        self.db.mysql.close()
        self.db.ssh.close()

    def test_add_vehicle(self):
        """
        a   车牌号
        b   车辆类型
        c   挂车类型
        d   车辆道路运输证正面
        e   运输证证件有效截止日期
        f   代理证正面
        g   代理证反面
        h   车辆行驶证正本正面
        i   车辆行驶证正本反面
        j   车辆行驶证副本正面
        k   车辆行驶证副本反面
        l   车辆行驶证截至时间
        m   车辆识别代码
        n   车队id
        o   车队名称
        p   荷载吨数
        q   装口类型
        r   类型  1车辆  2挂车
        web   挂车号
        t   代理证时间
        """
        vehicle_num = provide_data.get_info('车辆')
        url = self.url + 'saas/res/car/add'
        param = {
            'a': vehicle_num,
            'b': 1,
            'd': 'JA65E76231074EEC048',
            'e': 1747670400000,
            'f': 'JA65E76231074EEC048',
            'g': 'JA65E76231074EEC048',
            'h': 'JA65E76231074EEC048',
            'i': 'JA65E76231074EEC048',
            'j': 'JA65E76231074EEC048',
            'k': 'JA65E76231074EEC048',
            'l': 1747670400000,
            'n': self.fleet_id,
            'r': 1
        }
        result = self.web.web_post(*self.fleet_login_result, url=url, param=param)
        assert result['a'] == '200'

    def test_add_trailer(self):
        trailer_num = provide_data.get_info('挂车')
        url = self.url + 'saas/res/car/add'
        param = {
            'web': trailer_num,
            'c': random.randint(1, 5),
            'd': 'JA65E76231074EEC048',
            'e': 1747670400000,
            'f': 'JA65E76231074EEC048',
            'g': 'JA65E76231074EEC048',
            'h': 'JA65E76231074EEC048',
            'i': 'JA65E76231074EEC048',
            'j': 'JA65E76231074EEC048',
            'k': 'JA65E76231074EEC048',
            'l': 1747670400000,
            'm': trailer_num[1:-1],
            'n': self.fleet_id,
            'p': 33330,
            'q': '1',
            'r': 2
        }
        result = self.web.web_post(*self.fleet_login_result, url=url, param=param)
        assert result['a'] == '200'

    def test_add_driver(self):
        """
        a   车队ID
        b   司机姓名
        c   司机身份证号
        d   司机号码
        e   驾驶证正本正面
        f   驾驶证副本正面
        g   驾驶证副本正面
        h   从业资格证文件
        i   从业资格证有效期截止日期
        j   从业资格号码
        k   押运员证
        l   押运员证时间
        m   类型  1司机  2押运员
        """
        driver_info = provide_data.get_info('司机')
        url = self.url + 'saas/res/driver/add'
        param = {
            'a': self.fleet_id,
            'b': driver_info[0],
            'c': driver_info[2],
            'd': driver_info[1],
            'e': 'JE0B1F519007645B646',
            'f': 'JE0B1F519007645B646',
            'g': 1747670400000,
            'h': 'JE0B1F519007645B646',
            'i': 1747670400000,
            'j': str(driver_info[1]),
            'm': 1
        }
        result = self.web.web_post(*self.fleet_login_result, url=url, param=param)
        assert result['a'] == '200'

    def test_add_supercargo(self):
        supercargo_info = provide_data.get_info('押运员')
        url = self.url + 'saas/res/driver/add'
        param = {
            'a': self.fleet_id,
            'b': supercargo_info[0],
            'd': supercargo_info[1],
            'k': 'JE0B1F519007645B646',
            'l': 1747670400000,
            'm': 2
        }
        result = self.web.web_post(*self.fleet_login_result, url=url, param=param)
        assert result['a'] == '200'

    def test_add_capacity(self):
        url = self.url + 'saas/res/transport/add'
        param = {
            'a': self.fleet_id,
            'b': '车辆ID',
            'c': '挂车ID',
            'd': '司机ID',
            'e': '司机UID',
            'f': '押运员ID',
            'g': ''
        }
        result = self.web.web_post(*self.fleet_login_result, url=url, param=param)
        assert result['a'] == '200'

    def test_vehicle_list(self):
        self.log.info("-----> 开始查询车辆")
        url = self.url + 'saas/res/car/list'
        param = {
            'a': self.fleet_id,
            'd': 1,
            'x': 1,
            'y': 10
        }
        result = self.web.web_post(*self.fleet_login_result, url=url, param=param)
        assert result['a'] == '200'

    def test_trailer_list(self):
        url = self.url + 'saas/res/car/list'
        param = {
            'a': self.fleet_id,
            'd': 2,
            'x': 1,
            'y': 10
        }
        result = self.web.web_post(*self.fleet_login_result, url=url, param=param)
        assert result['a'] == '200'

    def test_driver_list(self):
        url = self.url + 'saas/res/driver/list'
        param = {
            'a': self.fleet_id,
            'd': 1,
            'x': 1,
            'y': 10
        }
        result = self.web.web_post(*self.fleet_login_result, url=url, param=param)
        assert result['a'] == '200'

    def test_supercargo_list(self):
        url = self.url + 'saas/res/driver/list'
        param = {
            'a': self.fleet_id,
            'd': 2,
            'x': 1,
            'y': 10
        }
        result = self.web.web_post(*self.fleet_login_result, url=url, param=param)
        assert result['a'] == '200'

    def test_capacity_list(self):
        url = self.url + 'saas/res/transport/list'
        param = {
            'a': self.fleet_id,
            'x': 1,
        }
        result = self.web.web_post(*self.fleet_login_result, url=url, param=param)
        assert result['a'] == '200'

    def test_issue_inquiry(self):
        """
        a   发货类型 1长途 2短途
        b   需求车数
        c   询价装货地
        d   询价卸货地
        e   货品名称
        f   装货时间
        g   数量
        h   开票类型 0-不开票 1-开票
        i   账期类型 1收到发票 2 对账完成 3 定日付款 4 收到磅单
        j   小五集合
        k   备注
        m   账期值
        n   货源来源 1 web 2 app 3 微服务 4 API
        o   单位 数据字典
        op_code     PG005
        op_ncode    230:PT007-->小五询价报价；230:PT023-->车队询价报价
        """
        o = random.randint(1, 3)
        g = random.randint(100, 10000)
        g = o == 1 and g * 1000 or g
        param = {
            "a": random.randint(1, 2),
            "b": random.randint(10, 1000),
            "c": self.rand.get_abbr_address(),
            "d": self.rand.get_abbr_address(),
            "e": random.choice(["雪碧", "可乐", "咖啡", "奶茶", "啤酒", "香槟"]),
            "f": random.randint(1585065600, 1591718400) * 1000,
            "g": g,
            "h": random.randint(0, 1),
            "i": random.randint(1, 4),
            "j": [{"a": 425296, "b": "小鱼儿"}],
            "k": self.word.fetchone_text(),
            "m": random.randint(1, 100),
            "n": 1,
            "o": o,
            "op_code": "PG005",
            "op_ncode": "230:PT007,230:PT023"
        }
        result = self.web.issue_inquiry(*self.service_login_result, param=param)
        assert result['a'] == '200'

    def test_issue_goods(self):
        """
        a   货单类型 1长途 2短途
        b   企业id
        c   装货地 三级联动
        d   卸货地 三级联动
        e   货品名称
        f   装货地别名
        g   数量
        h   需求车数
        i   损耗值
        j   卸货地别名
        k   货主价格
        l   是否开票 0不开票 1开票
        m   车队价格
        n   运费是否包含税点 1是 2否
        o   货品单价
        p   备注
        q   小五id集合 [{'a':小五用户id,'b':小五名称}]
        r   损耗方式 1千分比 2公斤
        web   详细装货地
        t   详细卸货地
        u   企业名称
        v   货源来源 1web  2app 3微服务 4API
        aa  账期值
        ab  结算方式 1数量  2批次  3期间
        ac  付款方式 1固定日期  2对账完成
        ad  计费方式 1单价（吨） 2里程（公里） 3次  4天
        ae  货品id
        af  装货时间
        ag  备注2
        ah  账期类型 1收到发票  2对账完成  3定日付款  4收到磅单
        ai  单位 1吨  2立方  3件
        aj  核算磅单 1装货 2卸货
        ak  结算值
        al  付款值
        op_code    PG010
        op_ncode   234:PT012,234:PT024
        """
        ai = random.randint(1, 3)
        g = random.randint(100, 1000)
        g = ai == 1 and g * 1000 or g
        r = random.randint(1, 2)
        i = r == 1 and random.randint(0, 3) or random.randint(0, 100)
        param = {
            "a": random.randint(1, 2),
            "b": 42,
            "c": self.rand.create_area_name(),
            "d": self.rand.create_area_name(),
            "e": random.choice(["雪碧", "可乐", "咖啡", "奶茶", "啤酒", "香槟"]),
            "f": self.rand.get_abbr_address(),
            "g": g,
            "h": random.randint(100, 1000),
            "i": i,
            "j": self.rand.get_abbr_address(),
            "k": random.randint(300, 500) * 100,
            "l": random.randint(0, 1),
            "m": random.randint(100, 300) * 100,
            "n": 1,
            "o": random.randint(1000, 9999) * 100,
            "p": self.word.fetchone_text(),
            "q": [{"a": 425296, "b": "小鱼儿"}],
            "r": r,
            "web": self.rand.get_detailed_address(),
            "t": self.rand.get_detailed_address(),
            "u": "南京君临天下科技有限公司",
            "v": 1,
            "aa": random.randint(1, 100),
            "ab": random.randint(1, 3),
            "ac": random.randint(1, 2),
            "ad": random.randint(1, 4),
            "ae": 1,
            "af": random.randint(1585065600, 1591718400) * 1000,
            "ah": random.randint(1, 4),
            "ai": ai,
            "aj": random.randint(1, 2),
            "ak": random.randint(1, 100),
            "al": random.randint(1, 100),
            "op_code": "PG010",
            "op_ncode": "313:PT012,313:PT024"
        }
        result = self.web.issue_goods_post(*self.service_login_result, param=param)
        assert result['a'] == '200'

    def test_confirm_inquiry(self):
        """
        a   货品名称
        b   货品单价
        c   询价id
        d   结算方式 1数量  2批次  3期间
        e   结算值
        f   装货地别名
        g   卸货地别名
        h   装货地 三级联动
        i   装货地详细地址
        j   卸货地 三级联动
        k   卸货地详细地址
        l   装货时间
        m   损耗方式  1千分比  2公斤
        n   损耗值
        o   发货数量类型  1顿  2立方  3件
        p   发货数量值
        q   上家运价
        r   是否开票  0不开票  1开票
        web   下家运价
        t   货主id
        u   货主名称
        v   需求车数
        aa  账期类型 1收到发票  2对账完成  3定日付款  4收到磅单
        ab  账期值
        ac  小五集合 [{'a':小五用户id,'b':小五名称}]
        ad  备注
        ae  来源 1web 2app 3微服务 4API
        af  核算榜单 1装货  2卸货
        ag  付款方式 1固定日期 2对账完成
        ah  付款值
        ai  计费方式
        """
        param = {
            'a': random.choice(['雪碧', '可乐', '咖啡', '奶茶']),
            'b': random.randint(1000, 9999) * 100,
            'c': 430,
            'd': 1,
            'e': '11',
            'f': self.rand.get_abbr_address(),
            'g': self.rand.get_abbr_address(),
            'h': self.rand.create_area_name(),
            'i': self.rand.get_detailed_address(),
            'j': self.rand.create_area_name(),
            'k': self.rand.get_detailed_address(),
            'l': 1584633600000,
            'm': 2,
            'n': 33,
            'o': 2,
            'p': 70300,
            'q': 55500,
            'r': 0,
            'web': 22200,
            't': 1,
            'u': '南京零距离科技有限公司',
            'v': 269,
            'aa': 2,
            'ab': 5,
            'ac': [{'a': 425296, 'b': '小鱼儿'}],
            'ad': self.word.fetchone_text(),
            'ae': 1,
            'af': 2,
            'ag': 1,
            'ah': 11,
            'ai': 1
        }
        result = self.web.confirm_inquiry(user_id=self.service_user_id, param=param)
        assert result['a'] == '200'

    def test_get_address(self):
        """
        a   前线id
        b   类型 1装货地址 2卸货地址
        c   页数
        d   每页条数
        e   地址名称 模糊查询
        """
        param = {
            'a': self.service_user_id,
            'b': 1,
            'c': 1,
            'd': 10
        }
        result = self.web.get_address(user_id=self.service_user_id, param=param)
        assert result['a'] == '200'

    def test_add_address(self):
        """
        参数名称    	参数说明                        是否必须
        a           主键id                         false
        b           前线id                         true
        c           三级联动                        true
        d           详细地址                        true
        e           类型 1装货地址 2卸货地址           true
        g           地址类型 1三级联动地址 2发货地址    true
        op_code    PG001
        """
        param = {
            'b': self.service_user_id,
            'c': self.rand.create_area_name(),
            'd': self.rand.get_detailed_address(),
            'e': 2,
            'g': 1,
            "op_code": "PG001"
        }
        result = self.web.add_address(user_id=self.admin_user_id, param=param)
        assert result['a'] == '200'

    def test_query_inquiry_list(self):
        """
        a   询价单编号       false
        b   装货开始时间      false
        c   装货结束时间      false
        d   装货地           false
        e   卸货地           false
        f   页数
        g   每页条数
        h   状态 1:已处理 0-默认 2 取消
        i   询价id           false
        """
        url = self.url + 'saas/inquiry/manage/inquiryList'
        param = {
            "f": 1,
            "g": 10,
            "h": 0
        }
        result = self.web.web_post(*self.admin_user_id, url=url, param=param)
        assert result['a'] == '200'

    def test_query_goods_list(self):
        """
        b   企业id      false
        c   装货地
        d   卸货地
        e   装货开始时间
        f   装货结束时间
        g   货单状态
        h   货单编号    false
        x   第几页
        y   页大小
        """
        url = self.url + 'saas/goods/list/paging'
        param = {
            "x": 1,
            "y": 10
        }
        result = self.web.web_post(*self.admin_user_id, url=url, param=param)
        assert result['a'] == '200'

    def test_add_shipper(self):
        """
        a   来源 1-自注册 2-小五添加
        c   企业名称
        d   地址
        e   法人姓名
        f   法人身份证号
        g   企业类别
        h   三证合一号
        i   身份证图片正面
        j   身份证图片反面
        k   营业执照图片
        m   联系人姓名
        n   联系人电话
        t   联系人电话
        u   产品ID
        """
        url = self.url + 'saas/res/fleet/add'
        param = {
            "a": 2,
            "c": self.rand.get_company(),
            "d": self.rand.get_detailed_address(),
            "e": self.rand.get_name(),
            "f": self.rand.create_IDcard(),
            "h": self.rand.get_phone(),
            "i": "J83D8FE62B0C3A0737D",
            "j": "J83D8FE62B0C3A0737D",
            "k": "J83D8FE62B0C3A0737D",
            "m": self.rand.get_name(),
            "n": self.rand.get_phone(),
            "t": "123456",
            "u": 2020,
            "businessBool": True,
            "carTypeBool": False,
            "srcList": [],
            "businessUrlBool": True,
            "businessLinceBool": False,
            "frontList": [],
            "frontUrlBool": True,
            "frontPhotoBool": False,
            "idCardList": [],
            "idCardUrlBool": True,
            "idCardNationalBool": False
        }
        result = self.web.web_post(*self.admin_user_id, url=url, param=param)
        assert result['a'] == '200'
