import requests
import json
import time
import traceback #追踪异常
import pymysql
import sys
from selenium.webdriver import Firefox,FirefoxOptions

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

def get_baidu_hot():
    """
    ：return：返回百度疫情热搜
    """
    #爬取的网站
    url = "https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1"

    option = FirefoxOptions()#创建谷歌浏览器实例
    option.add_argument("--headless")#隐藏浏览器，加快爬取东西的速度
    option.add_argument("--no--sandbox") #禁用sandbox

    browser = Firefox(executable_path="/usr/lib/firefox/geckodriver",options=option)
    browser.get(url)
    #print(browser.page_source)


    dl = browser.find_element_by_css_selector('#ptab-0 > div > div.VirusHot_1-5-4_32AY4F.VirusHot_1-5-4_2RnRvg > section > div')
    #点击展开，显示剩余的热搜信息
    dl.click()
    time.sleep(1) #等待一秒

    #通过Xpath路径访问想要的东西，ctrl+f:查看对应的路径消息
    c = browser.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[2]/section/a/div/span[2]')
    context = [i.text for i in c] #获取标签中的内容
    # print(context)查看输出的内容
    return context


def update_hotsearch():
    """
    将获取到的疫情热搜数据插入到hotsearch数据库中
    :return: 没有返回值
    """
    cursor = None
    conn = None
    
    try:
        context = get_baidu_hot()#调用刚刚写好东西
        print(f"{time.asctime()}开始更新热搜数据")
        conn, cursor = get_conn()
        sql1 = "TRUNCATE table hotsearch;"#更新之前先将所有数据删除
        cursor.execute(sql1)
        print(f"{time.asctime()}清空数据完毕")
        sql = "insert into hotsearch(dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X") #将时间处理为当前格式
        for i in context:
            cursor.execute(sql,(ts, i)) #插入数据(时间，内容)
        conn.commit()#提交事务
        print(f"{time.asctime()}数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)

if __name__ == "__main__":
    l = len(sys.argv)
    if l == 1:
        s = """
        请输入参数
        参数说明：  
        up_his  更新历史记录表
        up_hot  更新实时热搜
        up_det  更新详细表
        """
        print(s)
    else:
        order = sys.argv[1]
        if order == "up_his":
            update_history()
        elif order == "up_det":
            update_details()
        elif order == "up_hot":
            update_hotsearch()
  