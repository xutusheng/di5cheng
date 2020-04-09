# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/6
# @PROJECT : di5cheng-IT-AUV
# @File    : service.py

import requests
from common.logger import MyLog
from common import config

null = None

url_service = config.get_url()


class Service:

    global null

    def userlogin(self, a, b):
        # 登录
        url = url_service + "paas/mm/userlogin?md=10&cmd=01"
        # 给密码进行MD5加密
        b_md5 = config.get_md5(b)
        param = {"a": a, "b": b_md5}
        r = requests.post(url=url, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def queryUserBasicInfo(self, user_id):
        # 查询用户基本信息
        url = url_service + "saas/res/org/userInfo"
        headers = {"user_id": str(user_id)}
        param = {}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def queryUserMenu(self, user_id):
        # 查询用户菜单
        url = url_service + "saas/res/org/people/menu"
        headers = {"user_id": str(user_id)}
        param = {}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def queryCompanyOrgAllListByCompanyId(self, user_id, a):
        # 查询车队的组织架构信息
        url = url_service + "saas/res/company/org/all/list"
        headers = {"user_id": str(user_id)}
        param = {"a": a}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def addOrgPeople(self, cpy_id, a, c, d, e, f, h):
        # 新增部门人员
        url = url_service + "saas/res/org/people/add"
        headers = {"cpy_id": str(cpy_id)}
        param = {"a": a, "c": c, "d": d, "e": e, "g": 2020, "f": f, "h": h}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def editOrgPeople(self, user_id, a, c, d, f):
        # 修改部门人员
        url = url_service + "saas/res/org/people/edit"
        headers = {"user_id": str(user_id)}
        param = {"a": a, "c": c, "d": d, "f": f}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def queryCarList(self, user_id, a, d, x, y):
        # 查询车辆列表
        url = url_service + "saas/res/car/list"
        headers = {"user_id": str(user_id)}
        param = {"a": a, "d": d, "x": x, "y": y}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def queryCarDetail(self, user_id, a, b, c):
        # 查询车辆详情
        url = url_service + "saas/res/car/detail"
        headers = {"user_id": str(user_id)}
        param = {"a": a, "b": b, "c": c}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def addCar(self, user_id, n, r, a, b, m="", e="", l="", d="", f="", g="", h="", i="", j="", k=""):
        # 车辆添加
        url = url_service + "saas/res/car/add"
        headers = {"user_id": str(user_id)}
        param = {
            "a": a,
            "b": b,
            "d": d,
            "e": e,
            "f": f,
            "g": g,
            "h": h,
            "i": i,
            "j": j,
            "k": k,
            "l": l,
            "m": m,
            "n": n,
            "r": r
        }
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def carEdit(self, user_id, a, u, b, c, d, e, g, h, i, j, k, l, n, q):
        # 车辆信息修改
        url = url_service + "saas/res/car/edit"
        headers = {"user_id": str(user_id)}
        param = {
            "a": a,
            "b": b,
            "d": d,
            "e": e,
            "c": c,
            "g": g,
            "h": h,
            "i": i,
            "j": j,
            "k": k,
            "l": l,
            "u": u,
            "n": n,
            "q": q
        }
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def addguaCar(self, user_id, s, c, p, n, q, r, d="", f="", g="", e="", h="", i="", m="", l="", j="", k=""):
        # 挂车车辆添加
        url = url_service + "saas/res/car/add"
        headers = {"user_id": str(user_id)}
        param = {
            "s": s,
            "c": c,
            "d": d,
            "e": e,
            "f": f,
            "g": g,
            "h": h,
            "i": i,
            "j": j,
            "k": k,
            "l": l,
            "m": m,
            "n": n,
            "p": p,
            "q": q,
            "r": r
        }
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def guacarEdit(self, user_id, a, u, b, c, d, e, g, h, i, j, k, l, n, o, p, q):
        # 挂车信息修改
        url = url_service + "saas/res/car/edit"
        headers = {"user_id": str(user_id)}
        param = {
            "a": a,
            "b": b,
            "d": d,
            "e": e,
            "c": c,
            "g": g,
            "h": h,
            "i": i,
            "j": j,
            "k": k,
            "l": l,
            "u": u,
            "n": n,
            "o": o,
            "p": p,
            "q": q
        }
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def querydriverList(self, user_id, a, d, x, y, c=None):
        # 司机/押运员列表查询
        url = url_service + "saas/res/driver/list"
        headers = {"user_id": str(user_id)}
        param = {"a": a, "d": d, "x": x, "y": y, "c": c}
        if param["c"] is None:
            del param["c"]
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def addDriver(self, user_id, a, b, c, d, m, e="", f="", g="", h="", i="", j=""):
        # 司机新增
        url = url_service + "saas/res/driver/add"
        headers = {"user_id": str(user_id)}
        param = {
            "a": a,
            "b": b,
            "d": d,
            "e": e,
            "c": c,
            "f": f,
            "g": g,
            "h": h,
            "i": i,
            "j": j,
            "m": m
        }
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def modifyDriver(self, user_id, a, b, c, d, m, e, f, g, h, i, j):
        # 司机修改
        url = url_service + "saas/res/driver/edit"
        headers = {"user_id": str(user_id)}
        param = {
            "a": a,
            "b": b,
            "d": d,
            "e": e,
            "c": c,
            "f": f,
            "g": g,
            "h": h,
            "i": i,
            "j": j,
            "m": m
        }
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def addyaDriver(self, user_id, a, b, d, k="", l="", m=""):
        # 押运员新增
        url = url_service + "saas/res/driver/add"
        headers = {"user_id": str(user_id)}
        param = {
            "a": a,
            "b": b,
            "d": d,
            "k": k,
            "l": l,
            "m": m
        }
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def modifyEscort(self, user_id, a, b, d, k, l, m):
        # 押运员修改
        url = url_service + "saas/res/escort/edit"
        headers = {"user_id": str(user_id)}
        param = {
            "a": a,
            "b": b,
            "d": d,
            "k": k,
            "l": l,
            "m": m
        }
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def carQueryList(self, user_id, a, b=None):
        # 查询所有车辆（搜索下拉栏）
        url = url_service + "saas/res/car/query"
        headers = {"user_id": str(user_id)}
        param = {"a": a, "b": b}
        if b is None:
            del param["b"]
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def guaQueryList(self, user_id, a, b=None):
        # 查询所有挂车（搜索下拉栏）
        url = url_service + "saas/res/gua/query"
        headers = {"user_id": str(user_id)}
        param = {"a": a, "b": b}
        if b is None:
            del param["b"]
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def driverQueryList(self, user_id, a, b=None):
        # 查询所有司机（搜索下拉栏）
        url = url_service + "saas/res/driver/query"
        headers = {"user_id": str(user_id)}
        param = {"a": a, "b": b}
        if b is None:
            del param["b"]
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def escortQueryList(self, user_id, a, b=None):
        # 查询所有押运员（搜索下拉栏）
        url = url_service + "saas/res/escort/query"
        headers = {"user_id": str(user_id)}
        param = {"a": a, "b": b}
        if b is None:
            del param["b"]
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def addTransport(self, user_id, a, b, d, e, c=None, f=None, g=None):
        # 新增运力绑定关系
        url = url_service + "saas/res/transport/add"
        headers = {"user_id": str(user_id)}
        param = {
            "a": a,
            "b": b,
            "c": c,
            "d": d,
            "e": e,
            "f": f,
            "g": g
        }
        if c is None:
            del param["c"]
        if f is None:
            del param["f"]
        if g is None:
            del param["g"]
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def editTransport(self, user_id, a, b, d, e, c, f, g):
        # 修改运力绑定关系
        url = url_service + "saas/res/transport/edit"
        headers = {"user_id": str(user_id)}
        param = {
            "a": a,
            "b": b,
            "c": c,
            "d": d,
            "e": e,
            "f": f,
            "g": g
        }
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def delTransport(self, user_id, a):
        # 删除运力绑定关系
        url = url_service + "saas/res/transport/del"
        headers = {"user_id": str(user_id)}
        param = {"a": a}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def queryTransport(self, user_id, a, x):
        # 查询运力绑定关系
        url = url_service + "saas/res/transport/list"
        headers = {"user_id": str(user_id)}
        param = {"a": a, "x": x}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def addressAddOrUpdate(self, user_id, b, c, d, e, g, a=None):
        # 常用装卸货地址增加、修改
        url = url_service + "saas/goods/address/addOrUpdate"
        headers = {"user_id": str(user_id)}
        param = {"a": a, "b": b, "c": c, "d": d, "e": e, "g": g}
        if a is None:
            del param["a"]
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def addressDelete(self, user_id, a):
        # 常用装卸货地址删除
        url = url_service + "saas/goods/address/delete"
        headers = {"user_id": str(user_id)}
        param = {"a": a}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def addressFind(self, user_id, a, b, c, d, e=None):
        # 常用装卸货地址查询
        url = url_service + "saas/goods/address/find"
        headers = {"user_id": str(user_id)}
        param = {"a": a, "b": b, "c": c, "d": d, "e": e}
        if e is None:
            del param["e"]
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def companyFind(self, user_id):
        # 货主公司查询
        url = url_service + "saas/acc/company/find"
        headers = {"user_id": str(user_id)}
        param = {}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def x5List(self, user_id):
        # 查询小五列表
        url = url_service + "saas/res/x5/list"
        headers = {"user_id": str(user_id)}
        param = {}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def msDsFind(self, user_id):
        # 常用货品查询
        url = url_service + "saas/goods/msds/find"
        headers = {"user_id": str(user_id)}
        param = {}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def dictionaries(self, user_id):
        # 常用货品查询
        url = url_service + "saas/cfg/dictionary/codes"
        headers = {"user_id": str(user_id)}
        param = {"a": ["settle-type", "return-type", "pay-type", "price-type", "down-type", "unit-type", "pounds-type"]}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def fixedAdd(self, user_id, a, aa, ab, ac, ad, ae, af, ag, ah, ai, aj, ak, al, b, c, d, e, f, g, h, i, j, k, l, m,
                 n, o, p, q, r, s, t, u, v):
        # 发布报车货单
        url = url_service + "saas/goods/fixed/add"
        headers = {"user_id": str(user_id)}
        param = {"a": a,
                 "ae": ae,
                 "f": f,
                 "j": j,
                 "e": e,
                 "af": af,
                 "h": h,
                 "g": g,
                 "ai": ai,
                 "k": k,
                 "m": m,
                 "l": l,
                 "o": o,
                 "p": p,
                 "q": q,
                 "s": s,
                 "t": t,
                 "u": u,
                 "v": v,
                 "ah": ah,
                 "aa": aa,
                 "ad": ad,
                 "aj": aj,
                 "ac": ac,
                 "al": al,
                 "ab": ab,
                 "ak": ak,
                 "i": i,
                 "r": r,
                 "n": n,
                 "c": c,
                 "d": d,
                 "b": b,
                 "ag": ag}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def goodsStatus(self, user_id):
        # 货单状态查询
        url = url_service + "saas/cfg/dictionary/goods-status"
        headers = {"user_id": str(user_id)}
        r = requests.get(url=url, headers=headers)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def listPaging(self, user_id, x, y, a=None, b=None, c=None, d=None, g=None, e=None, f=None, h=None):
        # 获取货单分页列表
        url = url_service + "saas/goods/list/paging"
        headers = {"user_id": str(user_id)}
        param = {"h": h,
                 "b": b,
                 "a": a,
                 "c": c,
                 "d": d,
                 "g": g,
                 "x": x,
                 "y": y,
                 "e": e,
                 "f": f}
        if a is None:
            del param["a"]
        if b is None:
            del param["b"]
        if c is None:
            del param["c"]
        if d is None:
            del param["d"]
        if e is None:
            del param["e"]
        if f is None:
            del param["f"]
        if g is None:
            del param["g"]
        if h is None:
            del param["h"]
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def queryGoodsOrderDetail(self, user_id, a):
        # 查询主货单详情
        url = url_service + "saas/goods/goods/mainDetail"
        headers = {"user_id": str(user_id)}
        param = {"a": a}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def fleetGoodsReportPrice(self, user_id, a):
        # 车队货源报价列表
        url = url_service + "saas/transport/report/list"
        headers = {"user_id": str(user_id)}
        param = {"a": a}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def goodsUnderWayCarOrderList(self, user_id, b, x, y):
        # 小五货单待确认车单列表
        url = url_service + "saas/transport/dispatch/list/unconfirmed/carOrders"
        headers = {"user_id": str(user_id)}
        param = {"b": b, "x": x, "y": y}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def goodsConfirmedCarOrderList(self, user_id, b, x, y):
        # 小五货单已确认车单列表
        url = url_service + "saas/transport/dispatch/list/confirmed/carOrders"
        headers = {"user_id": str(user_id)}
        param = {"b": b, "x": x, "y": y}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def goodsCanceledCarOrderList(self, user_id, b, x, y):
        # 小五货单已确认车单列表
        url = url_service + "saas/transport/dispatch/list/canceled/carOrders"
        headers = {"user_id": str(user_id)}
        param = {"b": b, "x": x, "y": y}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def inquiryAdd(self, user_id, a, b, c, d, e, f, g, h, i, j, k, m, o, n):
        # 发布询价货单
        url = url_service + "saas/goods/inquiry/add"
        headers = {"user_id": str(user_id)}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f,
                 "g": g,
                 "h": h,
                 "i": i,
                 "j": j,
                 "k": k,
                 "m": m,
                 "o": o,
                 "n": n}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def inquiryManageList(self, user_id, f, g, h, a=None, b=None, c=None, d=None, e=None, i=None):
        # 前线客服询价管理
        url = url_service + "saas/inquiry/manage/inquiryList"
        headers = {"user_id": str(user_id)}
        param = {"a": a,
                 "b": b,
                 "c": c,
                 "d": d,
                 "e": e,
                 "f": f,
                 "g": g,
                 "h": h,
                 "i": i}
        if a is None:
            del param["a"]
        if b is None:
            del param["b"]
        if c is None:
            del param["c"]
        if d is None:
            del param["d"]
        if e is None:
            del param["e"]
        if i is None:
            del param["i"]
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def inquiryReportPrice(self, user_id, a, b, c, d):
        # 询价查看-查看报价列表
        url = url_service + "saas/inquiry/dispatch/inquiryReportPrice"
        headers = {"user_id": str(user_id)}
        param = {"a": a, "b": b, "c": c, "d": d}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response

    def queryConfirmedPrice(self, user_id, b):
        # 查询被确认的报价价格
        url = url_service + "saas/inquiry/confirm/confirmedPrice"
        headers = {"user_id": str(user_id)}
        param = {"b": b}
        r = requests.post(url=url, headers=headers, json=param)
        response = eval(r.text)
        MyLog().logger().info(response)
        return response
