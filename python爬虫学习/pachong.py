import requests
import json

url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
#url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
res = requests.get(url) #获取数据
# print(res.text)

#用json表示内容
d = json.loads(res.text)
#获取到相关的数据
print(d["data"])
data_all = json.loads(d["data"])

data_all.keys()
print(data_all.keys())
# print(data_all["lastUpdateTime"]) #上次更新时间
# print(data_all["chinaTotal"]) #当前汇总数据
# print(data_all["areaTree"])#记录的所有的地区
# print(len(data_all["areaTree"]))#输出有多少个地区
# print(data_all["chinaAdd"]) #新增的值
print(data_all["chinaDayList"]) 


# print(data_all["areaTree"][0].keys())
# print(data_all["areaTree"][0]["name"]) #输出中国
# print(data_all["areaTree"][0]["today"]) #输出今天的所有数据
# print(data_all["areaTree"][0]["total"]) #输出今天的所有的中国的所有的数据

#print(data_all["areaTree"][0]["children"]) #输出的是中国的所有在记录的省份
print(len(data_all["areaTree"][0]["children"])) #输出总共34个的省份

#输出所有的省份的名称：
for i in data_all["areaTree"][0]["children"]:
    print(i["name"])

#输出该省份的所有的县市：
for i in data_all["areaTree"][0]["children"][22]["children"]:
    print(i["name"])

def get_tecent_data():
    #返回历史数据和当日详细数据

    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_ohter"
    headers = {
        "user-agent":" Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    r = requests.get(url,headers) #获取数据
    res = json.loads(r.test) #json字符串转换成字典
    data_all = json.loads(res['data'])

    history = {} #字典表示history
    for i in data_all["chinaDayList"]:
        ds = "2020" + i["date"]





    






