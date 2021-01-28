import pymysql
conn = pymysql.connect('localhost', user='root', passwd='dsax', db='fishdata')
cursor = conn.cursor()
cursor.execute('drop table if exists zhoushang')
sql = """create table if not exists `zhoushang` (
         `id` int(11) not null auto_increment,
         `class` varchar(255) not null comment 'fish class',
         `length` float(11,3) comment 'mm',
         `width` float(11,3) comment 'mm',
         `thickness` float(11,3) comment 'mm',
         `weight` float(11,3) comment 'g',
         `resolution` varchar(255) not null comment 'the resolution of image',
         `creation time` varchar(255) not null comment 'the date image created',
         `picAddr` varchar(255) not null comment 'the path of picture',
         `camPara` varchar(255) not null comment 'the path of parameter of the camera taking picture',
         primary key (`id`)    
        ) engine=innodb default charset=utf8 auto_increment=0"""
cursor.execute(sql)
cursor.close()
conn.close()