# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/3
# @PROJECT : di5cheng-IT-PaaS
# @File    : SendEmail.py

import os
import smtplib
import os.path
from common import config
from common.logger import MyLog
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_email(report_file, report_name):
    with open(report_file, 'rb')as f:
        mail_body = f.read()

    # 创建一个带附件的邮件实例
    msg = MIMEMultipart()
    # 以测试报告作为邮件正文
    msg.attach(MIMEText(mail_body, 'html', 'utf-8'))
    report_file = MIMEText(mail_body, 'html', 'utf-8')
    # 定义附件名称（附件的名称可以随便定义，你写的是什么邮件里面显示的就是什么）
    report_file["Content-Disposition"] = 'attachment;filename=' + report_name
    msg.attach(report_file)  # 添加附件
    msg['Subject'] = '自动化测试报告:' + report_name  # 邮件标题
    msg['From'] = config.get_sender()  # 发件人
    msg['To'] = config.get_receiver()  # 收件人列表
    try:
        server = smtplib.SMTP(config.get_server())
        server.login(config.get_sender(), config.get_sender_pwd())
        server.sendmail(msg['From'], msg['To'].split(';'), msg.as_string())
        server.quit()
    except smtplib.SMTPException:
        MyLog.logger().error(u'邮件发送测试报告失败 at' + __file__)


def send_report():
    # 找到最新的测试报告
    report_list = os.listdir(config.get_report_path())
    report_list.sort()
    new_report = os.path.join(config.get_report_path(), report_list[-1])
    # 发送邮件
    create_email(new_report, report_list[-1])
