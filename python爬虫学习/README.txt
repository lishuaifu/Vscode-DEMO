此项目跟着b站老师学习对中国新型冠状病数据的分析

一.
对于爬虫学习了requests模板，urlib模板，beautifulsoup4解析，pymysql连接数据库，学会使用selenium模块实现对chrome和firefox的自动化访问
1.项目中包括beautifulsoup4这一块用于学习对请求得到的网页进行解析分析
2.pymysql用于和本地的数据库进行连接，并操作本地数据库，涉及到了游标cursor，连接connect，以及相关的sql语句
3.requests用于对爬虫爬取的网页获取

二.通过爬取相关的网页获取实时的热搜信息
1.resougoogle.py通过Google-Chrome和Chromedrive对网页进行爬虫，一定要记住驱动和浏览器的版本要匹配
驱动地址：https://npm.taobao.org/mirrors/chromedriver/在里面进行寻找，完成以后一定要配置路径进行访问
ubuntu18.04上安装google-chrome的相关操作：https://www.cnblogs.com/x54256/p/8403864.html和https://www.cnblogs.com/myvic/p/10324531.html

2.resougoogle2.py和resougoogle.py一样，如果你的linux服务器出现问题，则使用这个
3.resoufirefox.py通过Firefox和geckodriver驱动对网页进行爬虫，一定要记住驱动和浏览器的版本要匹配
驱动地址：https://github.com/mozilla/geckodriver/releases 在里面寻找相关的驱动。
linux下firefox位置：/usr/lib/firefox。

三.
yiqing.py实现对疫情数据的爬取

四.
spider.py将上面的一，二和三进行结合，并且部署在linux服务器上，实现时刻的对实时信息的爬取
spider1.py是完整的部署在服务器上的爬虫项目实现定时爬取。用到了crontab -e 进行定时任务
------
30 * * * * python3 /root/spider.py up_his >> /root/log_his 2>&1 &  
50 * * * * python3 /root/spider.py up_hot >> /root/log_hot 2>&1 &
59 * * * * python3 /root/spider.py up_det >> /root/log_det 2>&1 &
------
crontab -e的相关介绍地址：https://blog.csdn.net/xjw440/article/details/79719157 

六.数据库相关的操作
在mysql.text当中存放
在linux服务器上记得安装数据库
安装mysql数据库以及用navicat连接MySQL的操作要注意

1.linux服务器安装mysql操作 ：https://www.jb51.net/article/157282.htm
2.navicat远程连接数据库实现可视化的相关注意操作：
https://blog.csdn.net/weixin_44487722/article/details/90144252?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task

.



