#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import pymysql
from news import *
from application import patent

db = pymysql.connect("118.89.54.249", "spider", "spider", "spider")
cursor = db.cursor()

if __name__ == '__main__':
    while True:
        sql = "delete from NewsInfoTable where Content = \'[email protected]\'"
        cursor.execute(sql)
        print(sql)
        sql = "SELECT Category FROM Keyword"
        try:
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            print(results)
            for row in results:
                patent(row[0])
        except:
            # 发生错误时回滚
            db.rollback()
            message = "关键词信息获取异常！出错位置：1 出错文件：patent.py"
        sql = "SELECT * FROM NewsCompanyInfo"
        try:
            # 执行sql语句
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                list_company = row[0]
                list_url = row[1]
                list_category = row[2]
                print(list_company, list_url, list_category)
                extract(list_company, list_url, list_category)
        except:
            # 发生错误时回滚
            db.rollback()
        sql = "delete from NewsInfoTable where Content = \'[email protected]\'"
        cursor.execute(sql)
        time.sleep(60*60)