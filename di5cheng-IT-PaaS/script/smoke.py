# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/18
# @PROJECT : di5cheng-IT-PaaS
# @File    : smoke.py

import copy
import time
import random
from ctypes import *
from api import app, web
from common import random_param, ParseWord, config
from common.logger import MyLog

null = None


class Smoke:

    global null

    def __init__(self):
        # 初始化
        self.web = web.Web()
        self.url = config.get_url()
        self.log = MyLog().logger()
        self.rand = random_param.Random_param()
        self.word = ParseWord.ParseWord(config.get_word())

        self.library = cdll.LoadLibrary(config.get_library())
        self.app = app.Common()
        self.app.initSDK(library=self.library, init_info=config.get_app_url())

        # 客服登录
        self.service_login_result = self.web.user_login_web(19900000001, '123456')
        self.service_headers = {
            "token": self.service_login_result[0],
            "user_id": self.service_login_result[1],
            "cpy_id": "0",
            "dt_type": "1",
            "user_type": "4",
            "product_id": "2020",
        }
        # 小五登录
        self.xiaowu_login_result = self.web.user_login_web(19900000002, '123456')
        self.xiaowu_headers = {
            "token": self.xiaowu_login_result[0],
            "user_id": self.xiaowu_login_result[1],
            "cpy_id": "0",
            "dt_type": "1",
            "user_type": "5",
            "product_id": "2020"
        }
        # 调度登录
        login_info = self.app.app_login(library=self.library, username=19933330000, password=123456)
        self.dispatch_user_id = eval(login_info["pBody"])["i"]

        # # 车队登录
        # self.fleet_login_result = self.s.user_login_web(19933334444, '123456')
        # self.fleet_id = self.s.get_user_info(*self.fleet_login_result)

    def service_issue_goods(self):
        # 客服发布货单
        url = self.url + 'saas/gds/fixed/add'
        headers = copy.copy(self.service_headers)
        headers["op_code"] = "PG010"
        headers["op_ncode"] = "341:PT012,341:PT024"
        ai = random.randint(1, 3)
        g = random.randint(100, 1000)
        g = ai == 1 and g * 1000 or g
        r = random.randint(1, 2)
        i = r == 1 and random.randint(0, 3) or random.randint(0, 100)
        param = {
            "a": random.randint(1, 2),
            "b": 42,
            "c": [self.rand.create_area_name()],
            "d": [self.rand.create_area_name()],
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
            "s": [self.rand.get_detailed_address()],
            "t": [self.rand.get_detailed_address()],
            "u": "南京君临天下科技有限公司",
            "v": 1,
            "aa": random.randint(1, 100),
            "ab": random.randint(1, 3),
            "ac": random.randint(1, 2),
            "ad": random.randint(1, 4),
            "ae": 1,
            "af": random.randint(1586275200, 1591718400) * 1000,
            "ah": random.randint(1, 4),
            "ai": ai,
            "aj": random.randint(1, 2),
            "ak": random.randint(1, 100),
            "al": random.randint(1, 100),
            "op_code": "PG010",
            "op_ncode": "341:PT012,341:PT024"
        }
        result = self.web.web_post(url=url, headers=headers, param=param)
        assert result['a'] == '200'
        g_serial = result["d"]["b"]
        return g_serial

    def xiaowu_view_pending_goods(self):
        # 小五查看待处理货单，返回首个货单信息
        """
        参数：
        父元素	参数名	必选	类型	长度	描述	取值说明
        c	否	String	24	装货地
        d	否	String	24	卸货地
        h	否	String	24	货源编号
        x	是	int	24	第几页
        y	是	int	24	页大小

        返回参数说明
        父元素	参数名	必选	类型	长度	描述	取值说明
        data	是	--	0..10]	数据列表
        data	a	是	int	50	货源ID
        data	b	是	String	50	装货地
        data	c	是	String	50	卸货地
        data	d	是	String	50	货品
        data	e	是	long	50	装货时间
        data	f	是	int	50	货主单价
        data	h	是	int	50	需要车辆数
        data	i	是	long	50	创建时间
        data	j	是	int	50	状态	发货 1取消 2报停 3待确认 4已承运 5运输中 6运输完成 7已生成对账单 8关闭 -1
        data	l	是	int	50	计费方式
        data	m	是	int	4	数量
        data	n	是	int	4	单位	吨 1立方 2件 3
        data	o	是	String	4	企业名称
        data	x	是	String	4	货源编号
        data	q	是	String	4	扩展字段1
        data	bb	是	String	4	扩展字段2
        data	ab	是	String	4	结算方式
        data	ac	是	String	4	账期类型
        data	ad	是	String	4	账期值
        data	ae	是	String	4	结算值
        data	af	是	int	50	货品单价
        data	ag	是	int	50	货单来源 2前线货单 3 小五货源 (如果为3展示报价列表)
        data	ah	是	int	50	车队指导价
        status	是	状态码	200成功
        z	是	总条数
        """
        url = self.url + 'saas/tpt/pc/good/waitSystemGoods'
        headers = self.xiaowu_headers
        param = {
            "x": 1,
            "y": 10,
            "g": 1
        }
        result = self.web.web_post(url=url, headers=headers, param=param)
        assert result['a'] == '200'
        return result['d'][0]

    def xiaowu_view_fleet_list(self):
        # 小五在定向报车中查看车队列表，返回首个车队信息
        """
        参数：
        父元素	参数名	必选	类型	长度	描述	取值说明
        a	否	String	32	车队名称(模糊搜索条件)
        x	是	int	24	第几页
        y	是	int	24	页大小

        返回参数说明
        父元素	参数名	必选	类型	长度	描述	取值说明
        data	是	--	0..10]	数据列表
        data	a	是	String	32	车队联系人
        data	b	是	String	32	车队名称
        data	c	是	long	32	联系人手机号
        data	d	是	int	11	车队id
        z	是	总条数
        """
        url = self.url + 'saas/tpt/userBinding/list/fleets'
        headers = self.xiaowu_headers
        param = {
            "x": 1,
            "y": 10
        }
        result = self.web.web_post(url=url, headers=headers, param=param)
        assert result['a'] == '200'
        return result['d'][0]

    def xiaowu_view_dispatch_list(self):
        # 小五在定向报车中查看首个车单下的所有调度，返回调度信息
        """
        参数：
        父元素	参数名	必选	类型	长度	描述	取值说明
        a	是	int	12	货源id
        b	否	int	12	车队id
        x	是	string	4	第几页
        y	是	int	4	每页条数

        返回参数说明
        父元素	参数名	必选	类型	长度	描述	取值说明
        data	否	--	0..10]	数据列表
        data	a	是	int	4	调度id
        data	b	是	int	4	调度名称
        data	c	是	int	4	调度号码
        z	是	--	4	总记录数
        """
        url = self.url + 'saas/tpt/dispatch/reportcaruser'
        headers = self.xiaowu_headers
        good_info = self.xiaowu_view_pending_goods()
        fleet_info = self.xiaowu_view_fleet_list()
        param = {
            "a": good_info['a'],
            "b": fleet_info['d'],
            "x": 1,
            "y": 10
        }
        result = self.web.web_post(url=url, headers=headers, param=param)
        assert result['a'] == '200'
        return good_info, fleet_info, result['d']

    def xiaowu_assign_dispatch(self):
        # 小五对首个货单定向报车
        """
        参数：
        父元素	参数名	必选	类型	长度	描述	取值说明
        a	是	int	12	货源id
        b	是	int	12	上报车数
        c	是	int	12	报价金额
        d	是	int	12	车队集合
        d	a	是	int	12	车队id
        d	b	是	int	8	调度id
        d	c	是	int	4	车队名称
        d	d	是	int	4	调度名称
        d	e	是	int	4	小五id
        d	f	是	int	4	小五名称

        返回参数说明
        父元素	参数名	必选	类型	长度	描述	取值说明
        a	是	int	15	响应	状态 取消4 报停3 关闭-1 存在小五未绑定车队9 存在调度已经生成运单,不可定向10
        """
        good_info, fleet_info, dispatch_info = self.xiaowu_view_dispatch_list()
        # print(good_info, fleet_info, dispatch_info, sep='\n')
        url = self.url + 'saas/tpt/dispatch/dispatch/reportCar'
        headers = copy.copy(self.xiaowu_headers)
        headers["op_code"] = "PT012"
        headers["op_ncode"] = "359:PT009"
        param = {
            "a": good_info['a'],
            "b": 10,
            "c": good_info['f'],
            "d":
            [
                {
                    "a": fleet_info['d'],
                    "b": dispatch_info[0]['a'],
                    "c": fleet_info['b'],
                    "d": dispatch_info[0]['b']
                },
                {
                    "a": fleet_info['d'],
                    "b": dispatch_info[1]['a'],
                    "c": fleet_info['b'],
                    "d": dispatch_info[1]['b']
                }
            ],
            "op_code": "PT012",
            "op_ncode": "359:PT009"
        }
        result = self.web.web_post(url=url, headers=headers, param=param)
        assert result['a'] == '200'
        return fleet_info['d']

    def dispatch_view_my_goods(self, fleet_id):
        # 调度查看我的货源，返回首个货源的货源ID:gs_id
        result = self.app.trans_my_report_goods_list(library=self.library, a=fleet_id, x=1, y=10)
        first_gs_id = eval(result["pBody"])["d"][0]["g"]
        return first_gs_id

    def dispatch_view_transport_capacity(self, fleet_id):
        # 调度查看运力列表，返回首个运力信息

        result = self.app.trans_capacity_list(library=self.library, a=fleet_id, x=1)
        transport_capacity_info = eval(result["pBody"])["d"][0]
        return transport_capacity_info

    def dispatch_goods_report_car(self, good_id, fleet_id, transport_capacity_info):
        # 调度在我的货源-货源上报车辆
        car_id = transport_capacity_info["a"]
        car_num = transport_capacity_info["b"]
        driver_id = transport_capacity_info["e"]
        driver_name = transport_capacity_info["f"]
        driver_phone = transport_capacity_info["h"]
        driver_id_card = transport_capacity_info["i"]
        trailer_id = transport_capacity_info["c"]
        trailer_num = transport_capacity_info["d"]
        trailer_ton = transport_capacity_info["p"]
        supercargo_name = transport_capacity_info["m"]
        supercargo_phone = transport_capacity_info["l"]
        e = [{"b": car_id, "c": car_num, "d": trailer_id, "e": trailer_num, "f": trailer_ton, "g": driver_id,
              "h": driver_name, "i": driver_phone, "j": driver_id_card, "k": 0, "l": supercargo_name,
              "m": supercargo_phone}]
        self.app.trans_manifest_report_car(library=self.library, a=good_id, d=fleet_id, e=e)

    def service_view_relevant_good(self, g_serial):
        # 客服查看相应的货单信息，返回货单ID
        url = self.url + 'saas/gds/list/paging'
        headers = self.service_headers
        param = {
            "h": g_serial,
            "x": 1,
            "y": 10
        }
        result = self.web.web_post(url=url, headers=headers, param=param)
        assert result['a'] == '200'
        g_id = result["d"][0]["a"]
        return g_id

    def service_view_be_confirmed_car(self, g_id):
        # 客服查看待确认车辆，返回首个车单id
        url = self.url + 'saas/gds/goodsCar/list/master/unconfirmed/carOrders'
        headers = self.service_headers
        param = {
            "b": g_id,
            "x": 1,
            "y": 10
        }
        result = self.web.web_post(url=url, headers=headers, param=param)
        assert result['a'] == '200'
        car_list_id = result["d"][0]["a"]
        return car_list_id

    def service_confirm_car(self, car_list_id):
        # 客服确认车辆
        """
        参数：
        父元素	参数名	必选	类型	长度	描述	取值说明
        a	是	int	10	车单id
        b	是	int	是否以最新价运输 1否 2是

        返回参数说明
        父元素	参数名	必选	类型	长度	描述	取值说明
        status	是	int	15	响应
        """
        url = self.url + 'saas/gds/goodsCar/confirm'
        headers = copy.copy(self.service_headers)
        headers["op_code"] = "PG022"
        headers["op_ncode"] = "326:PT015"
        param = {
            "a": car_list_id,
            "op_code": "PG022",
            "op_ncode": "326:PT015"
        }
        result = self.web.web_post(url=url, headers=headers, param=param)
        assert result['a'] == '200'

    def dispatch_view_waybill(self, fleet_id):
        # 调度查看运单-进行中列表，返回首个运单信息的运单ID
        result = self.app.trans_waybill_list(library=self.library, a=fleet_id, c=1)
        first_waybill_id = eval(result["pBody"])["d"][0]["p"]
        return first_waybill_id

    def dispatch_view_car_waybill(self, waybill_id):
        # 调度查看运单中车单，返回车单列表信息
        result = self.app.trans_car_waybill_list(library=self.library, a=waybill_id)
        car_lists_info = eval(result["pBody"])["d"]
        return car_lists_info

    def dispatch_get_pound_list(self, car_lists_info):
        # 调度获取磅单列表
        pound_id_list = []
        for car_list in car_lists_info:
            if car_list["g"] == 2:
                car_list_id = car_list["a"]
                result = self.app.trans_get_bind_list(library=self.library, a=car_list_id)
                load_pound_id, unload_pound_id = eval(result["pBody"])["f"][0]["a"], eval(result["pBody"])["f"][1]["a"]
                pound_id_list.append((load_pound_id, unload_pound_id))
        return pound_id_list

    def dispatch_upload_pound_list(self, pound_id_list, pound_file):
        # 调度上传磅单（对已确认车辆）
        for pound_id in pound_id_list:
            self.app.trans_loading_unload_upload(library=self.library, a=pound_id[0], b=pound_file,
                                                 c=random.randint(20000, 30000), e=1, f=1)
            self.app.trans_loading_unload_upload(library=self.library, a=pound_id[1], b=pound_file,
                                                 c=random.randint(20000, 30000), e=2, f=1)

    def service_view_confirmed_car(self, g_id):
        # 客服查看已确认车辆
        url = self.url + 'saas/gds/goodsCar/list/master/confirmed/carOrders'
        headers = self.service_headers
        param = {
            "b": g_id,
            "x": 1,
            "y": 10
        }
        result = self.web.web_post(url=url, headers=headers, param=param)
        assert result['a'] == '200'
        confirmed_cars_info = result["d"]
        return confirmed_cars_info

    def service_confirm_receipt(self, confirmed_cars_info):
        # 客服确认收货
        url = self.url + 'saas/gds/goodsCar/receive'
        headers = copy.copy(self.service_headers)
        headers["op_code"] = "PG024"
        for car_info in confirmed_cars_info:
            if car_info["g"] == 5:
                param = {
                    "a": car_info["a"],
                    "op_code": "PG024"
                }
                self.web.web_post(url=url, headers=headers, param=param)

    def service_finish_good(self, g_id):
        # 客服货单完成
        url = self.url + 'saas/gds/order/finish/confirm'
        headers = copy.copy(self.service_headers)
        headers["op_code"] = "PG026"
        param = {
            "a": g_id,
            "op_code": "PG026"
        }
        result = self.web.web_post(url=url, headers=headers, param=param)
        assert result['a'] == '200'

    def test_case(self):
        # 客服发布货单
        g_serial = self.service_issue_goods()
        # 小五定向报车
        time.sleep(1)
        fleet_id = self.xiaowu_assign_dispatch()
        # 调度查看我的货源，返回首个货源的货源ID
        time.sleep(1)
        first_gs_id = self.dispatch_view_my_goods(fleet_id=fleet_id)
        # 调度查看运力列表，返回首个运力信息
        transport_capacity_info = self.dispatch_view_transport_capacity(fleet_id=fleet_id)
        # 调度在我的货源-货源上报车辆
        time.sleep(2)
        self.dispatch_goods_report_car(good_id=first_gs_id, fleet_id=fleet_id,
                                       transport_capacity_info=transport_capacity_info)
        # 客服查看相应的货单信息，返回货单ID
        g_id = self.service_view_relevant_good(g_serial=g_serial)
        # 客服查看待确认车辆列表，返回首个车单ID
        car_list_id = self.service_view_be_confirmed_car(g_id=g_id)
        # 客服确认车辆
        time.sleep(1)
        self.service_confirm_car(car_list_id=car_list_id)
        # 调度查看运单-进行中列表，返回首个运单信息的运单ID
        time.sleep(2)
        first_waybill_id = self.dispatch_view_waybill(fleet_id=fleet_id)
        # 调度查看运单中车单，返回车单列表信息
        time.sleep(1)
        car_lists_info = self.dispatch_view_car_waybill(waybill_id=first_waybill_id)
        # 调度获取磅单列表（对已确认状态）
        time.sleep(1)
        pound_id_list = self.dispatch_get_pound_list(car_lists_info=car_lists_info)
        # 调度上传磅单
        time.sleep(0.5)
        self.dispatch_upload_pound_list(pound_id_list=pound_id_list, pound_file="J00067D59835E731588")
        # 客服查看已确认车辆列表
        time.sleep(0.5)
        confirmed_cars_info = self.service_view_confirmed_car(g_id=g_id)
        # 客服确认收货
        self.service_confirm_receipt(confirmed_cars_info=confirmed_cars_info)
        # 客服货单完成
        self.service_finish_good(g_id=g_id)


if __name__ == '__main__':
    smoke = Smoke()
    smoke.test_case()
