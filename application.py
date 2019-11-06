#!/usr/bin/env python3
import time
import pymysql
import requests

db = pymysql.connect("118.89.54.249", "spider", "spider", "spider")
cursor = db.cursor()

def patent(keyword):
    url = "https://www.tiikong.com/patent/queryresult/getList.do"

    querystring = {"page": "1", "pageSize": "100",
                   "searchType": "IntelligentSearch", "previousId": "", "sort": "pubDate:DESC"}
    querystring.setdefault("search", "(检索关键字:"+keyword+")")
    print(querystring)
    headers = {
        'User-Agent': "PostmanRuntime/7.15.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "5e4b3e75-b8f9-4d9f-9959-84a205346ccd,508f2ce0-2633-4bcc-a66b-2cdb5eb36aa9",
        'Host': "www.tiikong.com",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    r =response.json()
    for k,v in r.items():
        if k == 'data':
            for each in v:
                x = each['abstracttextCN'].replace("<span class='highLightKeyword'>","")
                x= x.replace("</span>", "")
                str(each['inventorsuniqueName'])
                y =','.join(each['inventorsuniqueName'])
                print(each['titletextCN'])
                sql = "insert into spider.Application (Title,ApplyTime,AnnounceTime,Owner,Category,Content,Url) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (
                    each['titletextCN'], each['appDate'], each['pubDate'], y, keyword, x,'null')
                try:
                    # 执行sql语句
                    print(sql)
                    cursor.execute(sql)
                    # 执行sql语句
                    db.commit()
                except:
                    # 发生错误时回滚
                    db.rollback()
                    print("已经有这条数据了")


if __name__ == '__main__':
    while True:
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
        time.sleep(24*60*60)
