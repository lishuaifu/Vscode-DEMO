# vscodel快速注释：“CTRL+ /” ，取消注释：“CTRL + K + U”
from urllib import request
url = "http://www.baidu.com/"

#添加header信息，这是最基本的反爬措施,在里面添加一个Agent,header是一个字典，key,value
header = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
}
req = request.Request(url,headers=header) #两个参数url和headers
res = request.urlopen(req) #获取响应

print(res.info()) #响应头
print(res.getcode()) #返回响应的状态码
print(res.geturl()) #返回响应的页面的地址

html = res.read()
print(html)
html = html.decode("utf-8")
print(html)