# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2019/9/30
# @PROJECT : di5cheng-UT-Fleet-P
# @File    : ParseConfig.py

import os
import configparser

# 项目根目录
projectPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 邮箱配置
configPath = os.path.join(projectPath, "config", "cfg.ini")
conf = configparser.ConfigParser()
conf.read(configPath, encoding="utf-8")
smtp_server = conf.get("email", "smtp_server")
port = conf.get("email", "port")
sender = conf.get("email", "sender")
psw = conf.get("email", "psw")
receiver = conf.get("email", "receiver")


# 截图目录
exceptionPath = projectPath + "/report/screenshot"

# xml目录
xmlPath = projectPath + "/report/xml"

# html目录
htmlPath = projectPath + "/report/html"

# 驱动存放路径， 需要自己根据自己电脑的驱动为止修改
iePath = ''
chromePath = ''
fireFox = ''

# excel文件存放路径
excelPath = projectPath + "/data/excel/demo.xlsx"

# log文件存放路径
logPath = projectPath + "/logs"

# 测试用例部分列对应的列号
testCase_testCaseName = 2
testCase_testStepName = 4
testCase_testIsExecute = 5
testCase_testRunEndTime = 6
testCase_testResult = 7

# 用例步骤对应的列号
testStep_testNum = 1
testStep_testStepDescribe = 2
testStep_keyWord = 3
testStep_elementBy = 4
testStep_elementLocator = 5
testStep_operateValue = 6
testStep_testRunTime = 7
testStep_testResult = 8
testStep_testErrorInfo = 9
testStep_testErrorPic = 10
