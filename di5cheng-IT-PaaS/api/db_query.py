# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/3
# @PROJECT : di5cheng-IT-PaaS
# @File    : db_query.py

from common import db_connect


class DBQuery:

    def __init__(self):
        self.ssh = db_connect.ssh_connect()
        self.ssh.start()
        self.mysql = db_connect.mysql_connect(self.ssh)

    def querycarbycarnumber(self, car_number):
        # 通过车牌号码查询车辆信息
        QUERY_CAR_LIST = """
                select * from t_r_car_info a where a.type=1 and a.car_number = '%s '
                """ % car_number
        return QUERY_CAR_LIST

    def queryguacarbycarnumber(self, gua_number):
        # 通过车牌号码查询挂车信息
        QUERY_CAR_LIST = """
                select * from t_r_car_info a where a.type=2 and a.gua_number = '%s '
                """ % gua_number
        return QUERY_CAR_LIST

    def querycarbycompany(self, company_id):
        # 通过公司id查询公司所有车辆（包括挂车）
        QUERY_CAR_LIST = """
                       select * from t_r_car_info a where a.id in 
                       (SELECT biz_id FROM t_r_company_car b where b.company_id = %d)
                        """ % company_id
        return QUERY_CAR_LIST

    def querydrivercarbycompany(self, company_id):
        # 通过公司id查询公司所有车辆
        QUERY_CAR_LIST = """
                       select * from t_r_car_info a where a.id in 
                       (SELECT biz_id FROM t_r_company_car b where b.company_id = %d ) and a.type = 1
                        """ % company_id
        return QUERY_CAR_LIST

    def queryguacarbycompany(self, company_id):
        # 通过公司id查询公司所有挂车
        QUERY_CAR_LIST = """
                       select * from t_r_car_info a where a.id in 
                       (SELECT biz_id FROM t_r_company_car b where b.company_id = %d ) and a.type = 2
                        """ % company_id
        return QUERY_CAR_LIST

    def querycarcertinfobybizid(self, biz_id):
        # 根据车辆(挂车)编号查询车辆(挂车)证件表
        QUERY_CAR_CERT_INFO = """
                        select * from t_r_car_cert_info a where a.biz_id= %d
                              """ % biz_id
        return QUERY_CAR_CERT_INFO

    def querydriverinfobyid(self, id, type):
        # 根据编号查询司机押运员表
        QUERY_DRIVER_INFO = """
                        select * from t_r_driver_info a where a.id= %d and a.type =  %d
                              """ % id, type
        return QUERY_DRIVER_INFO

    def querydrivercertinfobyid(self, biz_id):
        # 根据编号查询司机押运员证件表
        QUERY_DRIVER_INFO = """
                        select * from t_r_driver_cert_info a where a.biz_id= %d 
                              """ % biz_id
        return QUERY_DRIVER_INFO

    def querytransportinfobyid(self, company_id):
        # 根据公司id查询运力
        QUERY_TRANSPORT_INFO = """
                        select * from t_r_company_transport a where a.company_id= %d 
                              """ % company_id
        return QUERY_TRANSPORT_INFO

    def queryaddressinfobyuserid(self, user_id, address_sort):
        # 根据用户id查询常用装/卸货地址
        QUERY_TRANSPORT_INFO = """
                        select * from t_g_goods_address a where a.user_id= %d  and address_sort = %d
                              """ % user_id, address_sort
        return QUERY_TRANSPORT_INFO

    def querygoodsorderinfobyorderid(self, g_serial):
        # 根据货单编号查询货单主表
        QUERY_GOODSORDER_INFO = """
                              select * from t_g_goods_order a where a.g_serial= '%s'
                                    """ % g_serial
        return QUERY_GOODSORDER_INFO

    def queryinquiryinfobyorderid(self, inquiry_no):
        # 根据货单编号查询货单主表
        QUERY_INQUIRY_INFO = """
                              select * from t_g_goods_inquiry a where a.inquiry_no= '%s'
                                    """ % inquiry_no
        return QUERY_INQUIRY_INFO
