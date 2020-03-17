#爬取相关网站信息，并且将该网站的信息存入数据库中，最后将该文件转换成csv格式的文件。
from bs4 import BeautifulSoup
import requests
import csv
import time
import re    #是基于正则表达式的，Python中re模块基本用法解析
import random
import traceback #追踪异常
import pymysql
import pandas  as  pd
import os

#获取的是恋家的网站的数据进行分析
def get_rentfile():
    headers = {
        "user-agent":" Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }

    page = 1
    url = 'https://bj.lianjia.com/ditiezufang/pg' + str(page) + '/#contentList'
    details = []

    while page<= 10:
        time.sleep(2) #等待两秒钟
        res = requests.get(url,headers) 
        print(res.status_code)
        html = res.text
        soup = BeautifulSoup(html,'html.parser')

        items = soup.find_all('div',class_='content__list--item--main')
        for item in items:
            title = item.find('p',class_='content__list--item--title twoline').find('a').text
            if '青年公寓' in title:
                continue
            #print(type(title)) #title是字符串类型的数据
            add = re.findall('.*?·(.*?) .*',title)[0]
            #add1 = re.findall('.*?·(.*?) .*',title)
            #print(add1)通过这一步可以分析得出add1是一个列表类型的对象，所以需要用[0]将数据信息提取出来。
            price = item.find('em').text
            link = 'https://bj.lianjia.com' + item.find('p',class_='content__list--item--title twoline').find('a')['href']
            details.append([title,add,price,link])#将这个元素加入到details列表的末尾（也就是插入到列表中数据）
        page += 1

    return details


def get_conn():
    
    conn = pymysql.connect(host="localhost",user="root",password="123456",db="gaode")
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def insert_rent():
    """
    插入rent租房信息表
    ：return:
    """
    cursor = None
    conn = None
    try:
        li = get_rentfile() #0 是历史数据字典，1 最新详细数据列表
        conn, cursor = get_conn()  #通过定义的方法获得
        sql = "insert into rent(信息,position,rentmoney,Website) values (%s,%s,%s,%s)" 
        sql1 = "TRUNCATE table rent;"#更新之前先将所有数据删除"
        print(f"{time.asctime()}将表中的数据删除")
        cursor.execute(sql1)
        print(f"{time.asctime()}开始插入数据")
        for item in li:
            cursor.execute(sql, item)
            conn.commit()
        print(f"{time.asctime()}数据插入完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

# insert_rent()

def JoinDB():

    conn = None
    cursor = None

    conn, cursor = get_conn()  
    count=cursor.execute('select * from rent')
    print('总共有%s条数据' %count)
    # 搜取所有结果
    results = cursor.fetchall()
    # 获取表的数据结构字段
    fields = cursor.description
    return list(results), list(fields)
S=JoinDB()
# print(S[0][i])
# print(S[1][i][0])
results=S[0]
fields=S[1]
# print(results)
# print(fields)
# print(fields[0][0])
# print(results)
# #写入文件
def writer_file(results,fields):
    ##查看文件大小
    file_size = os.path.getsize('D:\python\高德API + Python3 解决租房问题\\tryserver\\rent1.csv')
    if file_size == 0:
        ##表头
        name=[]
        results_list=[]
        for  i  in  range(len(fields)):
            name.append(fields[i][0])
        # print(name)
        for  i  in  range(len(results)):
            results_list.append(results[i])
        ##建立DataFrame对象
        file_test = pd.DataFrame(columns=name, data=results_list)
        ##数据写入,不要索引
        file_test.to_csv('D:\python\高德API + Python3 解决租房问题\\tryserver\\rent1.csv', encoding='utf-8', index=False)
    else:
        with  open('D:\python\高德API + Python3 解决租房问题\\tryserver\\rent1.csv', 'a+', newline='') as  file_test:
            ##追加到文件后面
            writer = csv.writer(file_test)
            ##写文件
            writer.writerows(results)
            
insert_rent()
writer_file(results,fields)
get_rentfile()

