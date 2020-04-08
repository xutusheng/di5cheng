import unittest, os, time, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from HTMLTestRunner import HTMLTestRunner
from config import readConfig


def add_case(cur_path):
    """第一步：加载所有的测试用例"""
    case_path = os.path.join(cur_path, "case")
    discover = unittest.defaultTestLoader.discover(case_path, pattern="test*.py")
    return discover


def run_case(all_case, report_path):
    """第二步：执行所有的用例，并把结果写入HTML测试报告"""
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    if not os.path.exists(report_path):
        os.mkdir(report_path)
    report_abspath = os.path.join(report_path, now+"_result.html")
    fp = open(report_abspath, "wb")
    runner = HTMLTestRunner(stream=fp, title="测试报告", description="用例执行情况", verbosity=2)
    runner.run(all_case)
    fp.close()


def get_report_file(report_path):
    """第三步：获取最新的测试报告"""
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
    report_file = os.path.join(report_path, lists[-1])
    return report_file


def send_mail(report_file, sender, psw, receiver, smtp_server, port):
    """第四步：发送最新的测试报告内容"""
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


if __name__ == "__main__":
    cur_path = os.path.join(os.path.dirname(__file__))
    report_path = os.path.join(cur_path, "report")
    # 加载用例
    all_case = add_case(cur_path)
    # 执行用例
    run_case(all_case, report_path)
    # 获取最新测试报告
    report_file = get_report_file(report_path)
    # 邮箱配置
    smtp_server = readConfig.smtp_server
    port = readConfig.port
    sender = readConfig.sender
    psw = readConfig.psw
    receiver = readConfig.receiver
    send_mail(report_file, sender, psw, receiver, smtp_server, port)
