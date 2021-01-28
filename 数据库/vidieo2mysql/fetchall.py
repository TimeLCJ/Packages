import pymysql
conn = pymysql.connect('localhost', user='root', passwd='dsax')
conn.select_db('fishdata')
cur = conn.cursor()

# insert = cur.execute("insert into fishdata values(1,'tom',18)")
# print('添加语句受影响的行数：',insert)

cur.execute('select * from zhoushang')
#取所有数据
resTuple=cur.fetchall()
print(type(resTuple))
print('共%d条数据'%len(resTuple))
print(resTuple)

cur.close()
conn.close()
print('sql执行成功')