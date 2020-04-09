# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/16
# @PROJECT : di5cheng-IT-PaaS
# @File    : app.py

import json
import time
from ctypes import *
from threading import Event
from common.logger import MyLog

response = {}
event = Event()
c_back = bytes('               ', encoding="utf-8")


class Common:

    @staticmethod
    def sdk_callback(iMid, iCmd, iErr, pBody, pMsgID, iLen):
        param = {"iMid": iMid,
                 "iCmd": iCmd,
                 "iErr": iErr,
                 "pBody": pBody.decode('utf-8'),
                 "pMsgID": pMsgID,
                 "iLen": iLen
                 }
        global response
        response = param
        if param["iMid"] != 0:
            event.set()

    @staticmethod
    def get_response(iCmd):
        global response
        for n in range(20):
            result = response
            MyLog().logger().info(result)
            if result["iCmd"] != iCmd:
                time.sleep(1)
                continue
            else:
                return result

    CMPRESULTFUNC = CFUNCTYPE(None, c_int, c_int, c_int, c_char_p, c_char_p, c_int)
    CMPRESULTFUNC.restype = c_char_p
    PRESULTFUNC = CMPRESULTFUNC(sdk_callback)

    def initSDK(self, library, init_info):
        library.InitSDK.argtype = c_char_p
        library.InitSDK(init_info)
        library.SetNetState(1)
        library.RegistNotifyCallBack.restype = c_char_p
        global PRESULTFUNC
        PRESULTFUNC = self.CMPRESULTFUNC(self.sdk_callback)
        library.RegistNotifyCallBack(PRESULTFUNC)

    def app_register(self, library, phone, password, name, code, device_uid=None):
        # app调注册接口
        if device_uid is None:
            param = {"m": phone, "w": password, "n": name, "c": code, "a": "9417B966-5CC6-4E54-A32A-CB9D06FC2CA1"}
        else:
            param = {"m": phone, "w": password, "n": name, "c": code, "a": device_uid}
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x10, 0x06, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x06)

    def app_code(self, library, phone):
        # app获取短信验证码
        param = {
            "m": phone,
            "p": 100,
            "n": 3,
            "o": 1,
            "c": 3
        }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x10, 0x04, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x04)

    def app_login(self, library, username, password):
        # app调登录接口
        param = "{w:%s,i:192.168.4.114,d:94-DE-80-77-81-F1,p:100,h:3,o:1,c:2,e:%s,l:1}" % (password, username)
        c_param = bytes(param, encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x10, 0x01, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x01)

    def app_login_out(self, library):
        # app退出登录接口
        param = ""
        c_param = bytes(param, encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x12, 0x02, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x02)

    def trans_manifest_list(self, library, x, y, b=None, c=None):
        # 货源大厅列表
        """
        名称	约束	类型	长度	描述
        x	1	Int	4	page
        y	1	Int	4	pageSize
        b	0	String	本地手动输入搜索装货地
        c	0	String	本地手动输入搜索卸货地
        """
        param = {
            "x": x,
            "y": y,
            "b": b,
            "c": c
        }
        if b is None:
            del param["b"]
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x35, 0x10, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x10)

    def trans_manifest_detail(self, library, a):
        # 货单大厅详情
        """
        名称	约束	类型	长度	描述
        a	1	int		货源id
        """
        param = {
            "a": a
        }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x35, 0x11, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x11)

    def trans_my_report_list(self, library, a, b, x, y):
        # 我的货源-询价列表
        """
        名称	约束	类型	长度	描述      取值说明
        a	1	int	4	车队id	当前登录用户所属车队
        b	1	Int	4	调度id	当前登录用户userId
        x	1	int	4	page	分页,从1开始
        y	1	int	4	pageSize
        """
        param = {
            "a": a,
            "b": b,
            "x": x,
            "y": y
        }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x35, 0x12, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x12)

    def trans_my_report_detail(self, library, i, j):
        # 我的货源-询价详情
        """
        名称	约束	类型	长度	描述
        i	1	int	10	询价单id
        j	1	Int	10	调度id
        """
        param = {
            "i": i,
            "j": j
        }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x35, 0x13, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x13)

    def trans_my_report_goods_list(self, library, a, x, y):
        # 我的货源-货源列表
        """
        名称	约束	类型	长度	描述
        a	1	Int		调度id	当前登录用户userId
        x	1	int	4	page	分页,从1开始
        y	1	int	4	pageSize
        """
        param = {
            "a": a,
            "x": x,
            "y": y
        }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x35, 0x2c, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x2c)

    def trans_my_report_goods_detail(self, library, a):
        # 我的货源-货源详情
        """
        名称	约束	类型	长度	描述
        a	是	int	4	报价id
        """
        param = {
            "a": a
        }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x35, 0x2d, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x2d)

    def trans_capacity_list(self, library, a, x, c=None):
        # 运力列表
        """
        请求
        父元素   元素	约束	类型	长度	描述
                x	是	int	4	page
                a	是	int	4	车队id
                c	0	String	车牌号搜索
        响应
        父元素   元素  约束 类型 长度 描述
                data是	[]
        data	a	是	int	24	车辆ID
        data	b	是	int	24	车牌号
        data	c	是	int	24	挂车ID
        data	d	是	int	24	挂车号
        data	e	是	int	24	司机ID
        data	f	是	int	24	司机名称
        data	g	是	int	24	司机UID
        data	h	是	int	24	司机电话
        data	i	是	int	24	司机身份证号
        data	j	是	int	24	押运员ID
        data	k	是	int	24	押运员UID
        data	l	是	int	24	押运员电话
        data	m	是	int	24	押运员名称
        """
        param = {
            "a": a,
            "x": x,
            "c": c
        }
        if c is None:
            del param["c"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x35, 0x23, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x23)

    def trans_truck_list(self, library, a, x, d):
        # 车辆列表
        """
        元素	约束	类型	长度	描述
        a	是	int	4	车队id
        x	是	int	4	第几页
        """
        param = {
            "a": a,
            "x": x,
            "d": d
        }
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x35, 0x1f, 0, 0, param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x1f)

    def trans_manifest_report_car(self, library, a, d, e):
        # 货源报车
        """
        请求
        父元素 元素 约束 类型    长度 描述
                a	1	int	    24	货单id
                d	1	int	    24	当前车队id
                e	1	--	    [1..10]
            e	b	1	int	    4	车辆id
            e	c	1	String	12	车牌号
            e	d	0	int	    4	挂车id
            e	e	0	String	12	挂车号
            e	f	0	int	    4	核载吨数
            e	g	1	int	    4	司机id
            e	h	1	String	32	司机姓名
            e	i	1	long	8	司机手机号
            e	j	1	String	18	司机身份证号
            e	k	0	int	    4	押运员id
            e	l	0	String	12	押运员姓名
            e	m	0	long	8	押运员手机号
            e	n	0	String	12	押运员身份证号
        响应
        父元素 元素 约束 类型    长度 描述       取值说明
                b	1	Int	    24	货源ID
                e	1	int	    24	车队ID
                f	1	Int	    24	调度ID
                g	1	String		车队名称
                h	1	String		调度名称
                i	1	int	    24	子货单ID
                a	1	--	    [1..5]车单ID
            a	a	1	Int	    24	车单ID
            a	b	1	Int	    24	车辆ID
            a	c	1	int	    4	返回状态	1：上报成功
                                            2：车辆运单未结束
                                            3：重复报车
                                            默认1
        """
        param = {
            "a": a,
            "d": d,
            "e": e
        }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x35, 0x1a, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x1a)

    def trans_waybill_list(self, library, a, c, x=None, y=None):
        # 运单列表
        """
        参数：
        父元素 参数名	必选	类型	长度	描述	    取值说明
                a	1	int	11	车队id
                x	0	int	11	page	不传默认第一页
                y	0	int	11	pageSize不传默认每页20条
                c	1	int	4	运单状态	1:进行中
                                        2:结束
                                        3:未签订协议
                                        4:结算中
                                        5:待付款
                                        6:付款结算
                                        7:异常
                                        10:运单对账结束
        返回参数说明
        父元素 参数名	必选	类型	    长度	    描述	        取值说明
                x	1	int		        页大小
                z	1	int		        总记录数
                w	1	int		        当前页
                data0	--	    0..10]	运单列表
        data	a	1	String	24	    运单编号
        data	b	1	int	    12	    运输单价
        data	c	1	int	    12	    承运车数
        data	d	1	int	    12	    承运总量
        data	e	1	int	    8	    是否多价0否1是
        data	f	1	int	    4	    是否开票0否 1是
        data	g	1	int	    4	    运单状态	    0:未确认;
                                                    1:进行中
                                                    2:结束
                                                    3:未签订协议
                                                    4:结算中
                                                    5:待付款
                                                    6:付款结算
                                                    7:异常
                                                    10:运单对账结束
        data	h	1	String		    装货地
        data	i	1	String	4	    卸货地
        data	j	1	String	24	    货品名
        data	k	1	long		    装货时间
        data	l	1	long		    运单生成时间
        data	m	1	int		        货源ID
        data	n	1	int		        货品数量
        data	o	1	int		        货源状态
        data	p	1	int		        运单ID
        """
        param = {
            "a": a,
            "c": c,
            "x": x,
            "y": y
        }
        if x is None:
            del param["x"]
        if y is None:
            del param["y"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x35, 0x14, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x14)

    def trans_car_waybill_list(self, library, a, x=None, y=None):
        # 运单车单列表
        """
        请求
        父元素 元素  约束   类型   长度 描述      取值说明
                a	1	int	    11	运单ID
                x	1	int	    11	Page页码	不传默认第一页
                y	1	int	    11	Pagesize每页条数	不传默认20条
        响应
        父元素 元素 约束   类型    长度 描述       取值说明
                x	1	int	    11	页大小
                z	1	int	    11	总记录数
                w	1	int	    11	当前页
                data	--			数据列表
        data	a	1	int		    车单ID
        data	b	1	String		挂车号
        data	c	1	String		车牌号
        data	d	1	String		司机名称
        data	e	1	String		手机号
        data	f	1	String		身份证号
        data	g	1	int		    车单状态	    101取消
                                                1待确认
                                                2已确认
                                                4运输中
                                                5已完成
        data	h	1	int		    多装货地
        data	i	1	int		    多卸货地
        data	j	1	int		    合单次数
        data	k	1	int		    类型
        """
        param = {
            "a": a,
            "x": x,
            "y": y
        }
        if x is None:
            del param["x"]
        if y is None:
            del param["y"]
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x35, 0x29, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x29)

    def trans_get_bind_list(self, library, a):
        # 磅单列表获取
        """
        请求
        父元素 元素  约束  类型 长度 描述      取值说明
                a	1	int	11	车单ID
                x	1	int	11	Page页码	不传默认第一页
                y	1	int	11	Pagesize每页条数	不传默认20条
        响应
        父元素 元素 约束   类型 长度 描述       取值说明
                x	1	int	11	页大小
                z	1	int	11	总记录数
                w	1	int	11	当前页
                data	--		数据列表
        data	a	1	String	地址
        data	b	1	int		类型	       1装 2卸
        data	c	1	int		预计承运数量
        data	d	1	int		单位
        data	e	1	int		顺序
        data	f	1	int		实际吨数
        data	g	1	String	磅单
        """
        param = {
            "a": a
        }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x35, 0x28, 0, a, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x28)

    def trans_loading_unload_upload(self, library, a, b, c, e, f):
        # 上传磅单
        """
        请求
        父元素 元素  约束   类型   长度 描述      取值说明
                a	1	int	    4	磅单ID
                b	1	String	24	磅单文件
                c	1	int	    4	数量
                e	1	int	    4	类型	    1：装货
                                            2：卸货
                f   1   int     4	类型     1：上传
                                            2：更新
        """
        param = {
            "a": a,
            "b": b,
            "c": c,
            "e": e,
            "f": f
        }
        c_param = bytes(json.dumps(param), encoding="utf-8")
        library.SendMsgRequest.argtypes = (c_int, c_int, c_int, c_int, c_char_p, c_char_p)
        library.SendMsgRequest(0x35, 0x18, 0, 0, c_param, c_back)
        event.wait()
        event.clear()
        return self.get_response(iCmd=0x18)
