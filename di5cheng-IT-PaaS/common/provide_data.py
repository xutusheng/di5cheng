# _*_ coding: utf-8 _*_
# @Author  : XuTusheng
# @Time    : 2020/3/17
# @PROJECT : di5cheng-IT-MSS
# @File    : provide_data.py

from common import ParseExcel


def get_info(sheet_name):
    excel = ParseExcel.ParseExcel()
    marks = excel.get_col_value(u'{}'.format(sheet_name), 1)
    count = 0
    for i in marks:
        if i == 1:
            count += 1
        else:
            break
    second = excel.get_col_value(u'{}'.format(sheet_name), 2)
    one_third = excel.get_cell_of_value(u'{}'.format(sheet_name), 1, 3)
    one_fourth = excel.get_cell_of_value(u'{}'.format(sheet_name), 1, 4)
    if one_third and one_fourth:
        third = excel.get_col_value(u'{}'.format(sheet_name), 3)
        fourth = excel.get_col_value(u'{}'.format(sheet_name), 4)
        excel.write_cell(u'{}'.format(sheet_name), count + 2, 1, 1)
        return second[count], third[count], fourth[count]
    elif one_third:
        third = excel.get_col_value(u'{}'.format(sheet_name), 3)
        excel.write_cell(u'{}'.format(sheet_name), count + 2, 1, 1)
        return second[count], third[count]
    else:
        excel.write_cell(u'{}'.format(sheet_name), count + 2, 1, 1)
        return second[count]


if __name__ == '__main__':
    print(get_info('押运员'))
