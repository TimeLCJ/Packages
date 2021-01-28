import pymysql
import os

conn = pymysql.connect('localhost', user='root', passwd='dsax', db='fishdata')
cursor = conn.cursor()

# fish parameter
name = 'Larimichthys crocea'
length = 107
width = 31
thickness = 16
weight = 18
resolution = '1280*720'
creation_time = '2020_10_16'
imgdir = './picture/Larimichthys crocea6'
parapath = './para/para_pi02_720.json'

content = []
# 确定id
cursor.execute('select * from zhoushang')
resTuple=cursor.fetchall()
if len(resTuple) == 0:
    id = 1
else:
    id = resTuple[-1][0] + 1
imgs = os.listdir(imgdir)
imgs.sort(key=lambda x: int(x[:-4]))
for i in imgs:
    imgpath = os.path.join(imgdir, i)
    content.append((id, name, length, width, thickness, weight, resolution, creation_time, imgpath, parapath))
    id += 1

#另一种插入数据的方式，通过字符串传入值
sql="insert into zhoushang values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql, content)

cursor.close()
conn.commit()
conn.close()
print('sql执行成功')