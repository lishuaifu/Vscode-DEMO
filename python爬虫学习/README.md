此项目跟着b站老师学习对中国新型冠状病数据的分析
一.
对于爬虫学习了requests模板，urlib模板，beautifulsoup4解析，pymysql连接数据库，学会使用selenium模块实现对chrome和firefox的自动化访问
1.项目中包括beautifulsoup4这一块用于学习对请求得到的网页进行解析分析
2.pymysql用于和本地的数据库进行连接，并操作本地数据库，涉及到了游标cursor，连接connect，以及相关的sql语句
3.requests用于对爬虫爬取的网页获取

二.通过爬取相关的网页获取实时的热搜信息
1.resougoogle.py通过Google-Chrome和Chromedrive对网页进行爬虫，一定要记住驱动和浏览器的版本要匹配
驱动地址：https://npm.taobao.org/mirrors/chromedriver/在里面进行寻找，完成以后一定要配置路径进行访问
2.resougoogle2.py和resougoogle.py一样，如果你的linux服务器出现问题，则使用这个
3.resoufirefox.py通过Firefox和geckodriver驱动对网页进行爬虫，一定要记住驱动和浏览器的版本要匹配
驱动地址：https://github.com/mozilla/geckodriver/releases 在里面寻找相关的驱动。



resougoogle.py



