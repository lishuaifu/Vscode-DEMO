from bs4 import BeautifulSoup  #BeautifulSoup会把复杂的HTML文档转换成一个树形结构，每个节点都是python的对象
import requests  #requests模块返回网页的响应
import re  #re是python自带的正则表达式模块，使用它需要一定的正则表达式的基础

url = "http://wsjkw.sc.gov.cn/scwsjkw/gzbd/fyzt.shtml"
res = requests.get(url)

#第一步，判断是否会出现乱码问题
#print(res.encoding)，查看当前网页的编码形式
#设置相应的编码方式为"utf-8"
res.encoding = "utf-8"
#print(res.headers)
#print(res.text)
html = res.text
soup = BeautifulSoup(html,'lxml')#这一步对请求得到的页面进行整理
#print(soup)
#通过soup获取h2标签的内容
#soup.find("h2".text) 

#查看a标签的
a = soup.find("a")
print(a)
print(a.attrs)
print(a.attrs["href"])

url_new = "http://wsjkw.sc.gov.cn"+a.attrs["href"]

res1 = requests.get(url_new)
res1.encoding = "utf-8"
soup = BeautifulSoup(res1.text,'lxml') 

#此处解析出来的context还是html格式，p标签中的内容
context = soup.find("p")
print(context)

#获取P标签中的具体的文本内容
text =context.text
print(text)

#此处运用一个正则表达式
patten = "新增治愈出院病例(\d+)例.*?疑似病例(\d+)例"  #.*后面叫做非贪心匹配

#re.search(regex,str)在str中查找满足条件的字符串，在刚刚获得的文本内容中寻找匹配内容
b =re.search(patten,text)
print(b)

b.groups()
print(b.groups()) #输出的是构成的一个组
print(b.group(0)) #输出的是正则表达式匹配的一个那句话
print(b.group(0),b.group(1),b.group(2)) #用1和2分别输出匹配的第一个和第二个