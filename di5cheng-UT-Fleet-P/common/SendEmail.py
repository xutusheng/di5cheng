# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/9/30
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : SendEmail.py

import smtplib
from common import ParseConfig
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 邮箱配置
smtp_server = ParseConfig.smtp_server
port = ParseConfig.port
sender = ParseConfig.sender
psw = ParseConfig.psw
receiver = ParseConfig.receiver


def send_mail(report_file):
    """发送最新的测试报告内容"""
    with open(report_file, "rb") as f:
        mail_body = f.read()
    # 定义邮件内容
    msg = MIMEMultipart()
    body = MIMEText(mail_body, _subtype="html", _charset="utf-8")
    msg['Subject'] = u"自动化测试报告"
    msg['From'] = sender
    msg['To'] = receiver
    msg.attach(body)
    # 添加附件
    att = MIMEText(mail_body, _subtype="base64", _charset="utf-8")
    att['Content-Type'] = "application/octet-stream"
    att['Content-Disposition'] = "attachment; filename='report.html'"
    msg.attach(att)
    try:
        smtp = smtplib.SMTP_SSL(smtp_server, port)
    except:
        smtp = smtplib.SMTP()
        smtp.connect(smtp_server, port)
    smtp.login(sender, psw)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
