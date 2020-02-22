import time
from id_validator import validator
Id_number = []

def get_date(year):
    # 因为身份证的格式为年日月为1985****
    layout = '%Y%m%d'
    # 获取第一天你和最后一天的时间元祖
    first_day = time.strptime(str(year) + '0101', layout)
    last_day = time.strptime(str(year) + '1231', layout)
    # 转换为时间戳
    first_day = time.mktime(first_day)  # 1514736000.0
    last_day = time.mktime(last_day)  # 1546185600.0
    # for循环第一天到最后一天，步长为3600*24(一天的秒数)
    for i in range(int(first_day), int(last_day) + 1, 3600 * 24):
        # 先localtime转换为时间元祖，然后strftime转换为需要的时间格式
        date = time.strftime(layout, time.localtime(i))  # 19850101 19850102..19851231
        # 将365种可能的身份证号码添加到列表
        Id_number.append('142431' + str(date) + '4810')
    return Id_number

def get_legal_Id_num(year):
    Id_number = get_date(year)
    for Id_num in Id_number:
        # 验证身份证的合法性
        result = validator.is_valid(Id_num)
        # 将合法的打印出来
        if result:
            print(Id_num)
		
get_legal_Id_num(1975)

#from id_validator import validator
#validator.get_info('142431194401294829') # 18 位 //这两句语句用来查看地区，
