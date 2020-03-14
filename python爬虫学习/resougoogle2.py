# -- coding: gbk --
#爬取热搜消息

#导入谷歌，谷歌配置,相当于模拟人自动操控浏览器
import time
import pymysql
import traceback #追踪异常
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



def get_baidu_hot():
    """
    ：return：返回百度疫情热搜
    """
    #爬取的网站
    url = "https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1" 
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver",
                          chrome_options=options)     

    driver.get(url)
    #print(browser.page_source)


    dl = driver.find_element_by_css_selector('#ptab-0 > div > div.VirusHot_1-5-4_32AY4F.VirusHot_1-5-4_2RnRvg > section > div')
    #点击展开，显示剩余的热搜信息
    dl.click()
    time.sleep(1) #等待一秒

    #通过Xpath路径访问想要的东西，ctrl+f:查看对应的路径消息
    c = driver.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[2]/section/a/div/span[2]')
    context = [i.text for i in c] #获取标签中的内容
    # print(context)查看输出的内容
    return context

#将获取的数据插入到数据库中

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

update_hotsearch()



    
