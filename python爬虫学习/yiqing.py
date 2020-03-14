import requests
import json
import time
import traceback #追踪异常
import pymysql

url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
url1 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
headers = {
    "user-agent":" Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
}

#此处连接的是url这个网站
r = requests.get(url,headers) #获取数据
res = json.loads(r.text)
data_all = json.loads(res["data"])

#此处连接的是url1这个网站
e = requests.get(url1,headers) 
res1 =json.loads(e.text)
data_all1 = json.loads(res1["data"])

#print(data_all1.keys())
#print(data_all.keys())



def get_tecent_data():
    #返回历史数据和当日详细数据

    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    headers = {
        "user-agent":" Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    r = requests.get(url,headers) #获取数据
    res = json.loads(r.text)
    
    data_all = json.loads(res["data"])
   
    # print(data_all.keys())
    # print(data_all['chinaDayList'])

    #获取的是history字典
    history = {} #字典表示history
    for i in data_all["chinaDayList"]:
        ds = "2020." + i["date"] #首先先修改格式为年月日
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup) #改变时间格式，不然插入数据库会报错，数据库是datetime类型
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm, "suspect":suspect, "heal":heal, "dead":dead}


    #获取的是detail列表，返回每个地方的总共确诊的，今天确诊的，总共治愈的，总共死亡的
    details = []
    update_time = data_all1["lastUpdateTime"]
    data_country = data_all1["areaTree"] #list25个国家
    data_province = data_country[0]["children"] #中国的34个省，市

    #通过循环访问每个省的每个地区
    for pro_infos in data_province:
        province = pro_infos["name"]
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm1 = city_infos["total"]["confirm"]
            confirm1_add = city_infos["today"]["confirm"]
            heal1 = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province, city, confirm1, confirm1_add, heal1, dead]) 
    # print(history)
    # print(details)        
    return history,details

get_tecent_data()


#pymysql

#定义好建立连接和关闭连接
def get_conn():

    conn = pymysql.connect(host="localhost",user="root",password="123456",db="cov")
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def update_details():
    """
    更新details表
    ：return:
    """
    cursor = None
    conn = None
    try:
        li = get_tecent_data()[1] #0 是历史数据字典，1 最新详细数据列表
        conn, cursor = get_conn()  #通过定义的方法获得
        sql = "insert into details(update_time, province, city, confirm, confirm_add, heal, dead) values (%s,%s,%s,%s,%s,%s,%s)" 
        sql_query = 'select %s = (select update_time from details order by id desc limit 1)' #对比当前最大时间戳，这里涉及后期的更新
        cursor.execute(sql_query,li[0][0]) #列表的第一条数据的第一条信息
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新最新数据")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新消息!")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def insert_history():
    """
    插入历史数据

    """
    cursor = None
    conn = None

    try:
        dic = get_tecent_data()[0] #0 是历史数据字典，1 最新详细数据列表
        print(f"{time.asctime()}开始插入历史数据")
        conn, cursor = get_conn()  #通过定义的方法获得
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        for k,v in dic.items():
            #item 格式{'2020-01-13':{'c'}}
            cursor.execute(sql,[k, v.get("confirm"),v.get("confirm_add"),v.get("suspect"),
                                v.get("suspect_add"),v.get("heal"),v.get("heal_add"),
                                v.get("dead"),v.get("dead_add")])

            conn.commit() #提交一下事务
            print(f"{time.asctime()}插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def update_history():
    """
    更新历史数据
    """
    cursor = None
    conn = None

    try:
        dic = get_tecent_data()[0] #0 是历史数据字典，1 最新详细数据列表
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()  #通过定义的方法获得
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        sql_query = "select confirm from history where ds=%s"
        for k,v in dic.items():
            #item 格式{'2020-01-13':{'confirm : 41','suspect': 0,'heal': 0, 'dead': 1}  }
            if not cursor.execute(sql_query, k):
                cursor.execute(sql,[k, v.get("confirm"),v.get("confirm_add"),v.get("suspect"),
                                v.get("suspect_add"),v.get("heal"),v.get("heal_add"),
                                v.get("dead"),v.get("dead_add")])

            conn.commit() #提交一下事务
            print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

#insert_history() #插入历史数据
update_details() #更新详细数据表
update_history() #更新历史数据