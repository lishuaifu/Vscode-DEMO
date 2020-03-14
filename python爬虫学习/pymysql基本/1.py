#pymysql

#建立连接
conn = pymysql.connect(host="localhost",user="root",password="123456",db="cov")

# #创建一个游标对象，默认是元组型
cursor = conn.cursor()

sql="select * from history"
#用游标执行这句话
cursor.execute(sql)
#获取所有的查询的结果
a = cursor.fetchall()
print(a)
#最后关闭
cursor.close()
conn.close

sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#当前时间的时间戳
cursor.execute(sql,[time.strftime("%Y-%m-%d"),10,1,2,3,4,5,6,7])
conn.commit()
b = cursor.fetchall()
print(b)

cursor.close()
conn.close
