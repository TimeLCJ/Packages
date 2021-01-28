import sqlite3
import cv2
import os


#连接到SQlite数据库
#数据库文件是test.db，不存在，则自动创建
db = sqlite3.connect('demodb_merged.db')
cursor = db.cursor()
cursor.execute('select * from fishmonitor order by id desc limit 1')
value = cursor.fetchall()
print(value)

start_id = value[0][0] + 1
new_db = []
img_path = './picture/lu-8-217-74-38-292_img/'
img_names = os.listdir(img_path)
img_names.sort(key=lambda x: int(x.split('.')[0]))
keys = img_path.split('/')[-2].split('-')
for i in img_names:
    new_db.append((start_id, 'Lateolabrax japonicus', keys[2], keys[3], keys[4], keys[5][:3], '2560*720', '2020_09_24', None, img_path+i))
    start_id += 1
print(new_db)
cursor.executemany('INSERT INTO fishmonitor VALUES (?,?,?,?,?,?,?,?,?,?)', new_db)


# cursor.execute('select * from fishmonitor')
# values = cursor.fetchall()
# print(values)
# (41, 'AA', 300, 120, 60, 915, '2560*720', '2020_09_24 11_41_45_086', None, './picture/pic2020_09_24 11_41_45_086.jpg')
# cursor.executemany('INSERT INTO fishmonitor VALUES (?,?,?,?,?,?,?,?,?,?)', values)

# commit
db.commit()
#关闭cursor
#关闭conn
cursor.close()
db.close()