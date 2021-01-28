import pymysql
conn = pymysql.connect('localhost', user='root', passwd='dsax')
conn.select_db('fishdata')
cur = conn.cursor()

cur.execute('select * from zhoushang')
print('删前数据为：')
for res in cur.fetchall():
    print(res)

cur.execute('delete from zhoushang where id=1')

cur.execute('select * from zhoushang;')
print('删后数据为：')
for res in cur.fetchall():
    print(res)
cur.close()
conn.commit()
conn.close()
print('sql执行成功')