import requests

url = "https://www.dianping.com"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
}
res = requests.get(url,headers=header)#注意requets不要和脚本名称相同
print(res)
print(res.encoding)
print(res.headers) #里面 如果没有Content-type，encoding就是utf-8,否则如果设置了charset,就以设置的为准，否则就是ISO-8859-1
print(res.url)

# print(res.text) 会有乱码问题
res.encoding = "utf-8" #解决了爬取的网页的乱码问题
#print(res.text) #输出网页的内容
print(res.status_code) #输出网页的响应码