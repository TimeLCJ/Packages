import pymysql
conn = pymysql.connect('localhost', user='root', passwd='dsax')
cursor = conn.cursor()
cursor.execute('create database if not exists fishdata default charset utf8 collate utf8_general_ci;')
cursor.close()
conn.close()