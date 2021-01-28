import pymysql
conn = pymysql.connect('localhost', user='root', passwd='dsax', db='fishdata')
cursor = conn.cursor()

# insert = cur.execute("insert into fishdata values(1,'tom',18)")
# print('添加语句受影响的行数：',insert)

#另一种插入数据的方式，通过字符串传入值
sql="insert into zhoushang values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.execute(sql,(1,'pomfret',20,20,20,10,'1280x720','2020-11-13','./','./'))

cursor.close()
conn.commit()
conn.close()
print('sql执行成功')