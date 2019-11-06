import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pymysql
import difflib
import list



#app = Celery('tasks', broker='redis://localhost:6379/0')

# mysql配置
db = pymysql.connect("118.89.54.249", "spider", "spider", "spider")
cursor = db.cursor()
#筛选内容
def check_content(url, text):
    if (not url) or (not text):
        return False

    if url.startswith("javascript"):
        return False

    if text.isdigit():
        return False

    if len(text.strip()) <= 10 or len(text.strip()) > 50:
        return False

    return True

#url处理
def complement_url(url, site):
    if not url.startswith("http"):
        base_url = urlparse(site).scheme + "://" + urlparse(site).netloc
        if url.startswith("./"):
            new_url = site.rstrip('/') + url[1:]
            return new_url

        if url.startswith("../..") or url.startswith("../"):
            url = url.lstrip("../")
            new_url = base_url + "/" + url
            return new_url

        if url.startswith("//www"):
            new_url = urlparse(site).scheme + ":" + url
            return new_url

        if url.startswith("//") and not url.startswith("//www"):
            new_url = base_url + url[1:]
            return new_url

        if url.startswith("/") and not url.startswith("//"):
            new_url = base_url + url
            return new_url

        if url.startswith("?"):
            new_url = base_url + urlparse(site).path + url
            return new_url
    else:
        return url

#爬网站信息 编码处理
def crawl(url):
    s = requests.session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
    }
    response = s.get(url, headers=headers, timeout=30)
    #text = CodingChange(response.text)

    if response.status_code == 200:
        text = response.text
        encoding = response.encoding
        apparent_encoding = response.apparent_encoding

        if encoding not in ['utf-8', 'UTF-8']:
            try:
                if apparent_encoding in ['utf-8', 'UTF-8', 'UTF-8-SIG']:
                    text = response.text.encode(encoding).decode('utf8')
                else:
                    if encoding == 'gb2312' and apparent_encoding == 'GB2312':
                        text = response.text.encode('utf8').decode('utf8')
                    elif encoding == 'ISO-8859-1' and apparent_encoding == 'ISO-8859-1':
                        text = response.text.encode('utf8').decode('utf8')
                    elif encoding == 'ISO-8859-1' and apparent_encoding == 'Big5':
                        text = response.text.encode(encoding).decode('big5').encode('utf8').decode('utf8')
                    elif encoding == 'big5' and apparent_encoding == 'Big5':
                        text = response.text.encode(encoding)
                        text = text.decode('big5')
                        text = text.encode('utf8')
                        text = text.decode('utf8')
                    else:
                        text = response.text.encode(encoding).decode('gbk').encode('utf8').decode('utf8')
            except:
                # log(ERROR, '编码错误 [{encoding}] [{url}]'.format(encoding=encoding, url=url))
                return False
        # save_html(text)
        return text
    return False


def diff_file(lines1, lines2):
    if (not lines1) or (not lines2):
        return
    diff_text = ''
    diff = list(difflib.ndiff(lines1.splitlines(), lines2.splitlines()))
    for i in diff:
        if i.startswith('+'):
            diff_text += i[1:]
    return diff_text



#将链接单独爬出来
def extract(company,crawlUrl,category):
    try:
        new_html_content = crawl(crawlUrl)
        diff_text = new_html_content
        soup = BeautifulSoup(diff_text,"lxml")
        items = soup.find_all('a')
        if items:
            for a in items:
                if a.string:
                    url, text = a.get('href'), a.string
                    check_pass = check_content(url, text)
                    if check_pass:
                        url = complement_url(url, crawlUrl)
                        if 'dfldjdfggwdt' in url:
                            continue
                        elif 'zhuanlan' in url:
                            continue
                        else:
                            sql = "insert into NewsInfoTable(Company, Url, Category, Content) VALUES ('%s', '%s', '%s','%s')" % (
                            company, url, category, text)
                            print(url + "    " + text)
                            try:
                                # 执行sql语句
                                cursor.execute(sql)
                                # 执行sql语句
                                db.commit()
                            except:
                                # 发生错误时回滚
                                print("已经有数据了")
                                db.rollback()

    except:
        print("#{id} {name} {site} {err}")



#单一网站输入
if __name__ == '__main__':
    sql = "SELECT * FROM NewsCompanyInfo"
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            list_company = row[0]
            list_url = row[1]
            list_category = row[2]
            print(list_company,list_url,list_category)
            extract(list_company, list_url, list_category)
    except:
        # 发生错误时回滚
        db.rollback()
    db.close()