# coding: utf-8

import sqlite3
import requests
import re
from bs4 import BeautifulSoup
import bs4
from random import randint
import time
import http.client
import schedule

def doSth():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'pgv_pvi=5512413184; qqmail_alias=guojin1@bupt.edu.cn',
        'Host': 'grs.bupt.edu.cn',
        'Referer': 'https://grs.bupt.edu.cn/list/list.php?p=16_1_2',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    }
    appKey = "R0owSVhtV1pNaVBhZFNDUDpOVGhydzdyWEJqRnhsemNI"
    # appKey = "QjRBMlJzeWYzMzJLU01vSjpZWHk5SFhQbWNvcW9uY1NR"
    headers2 = {
        'Proxy-Authorization': 'Basic ' + appKey,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'pgv_pvi=5512413184; qqmail_alias=guojin1@bupt.edu.cn',
        'Host': 'grs.bupt.edu.cn',
        'Referer': 'https://grs.bupt.edu.cn/list/list.php?p=16_1_1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    }
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]

    url = 'https://grs.bupt.edu.cn/list/list.php?p=16_1_1'
    response = requests.post(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    i = 1
    # print(soup)
    tt = soup.find('div', id="news").find('ul')

    #连接并更新数据库
    db = sqlite3.connect('test.db' )
    cursor = db.cursor()
    #cursor.execute('create table news_YJSY(title varchar(200) primary key,url varchar(200))')
    cursor.execute('delete from news_YJSY')

    for t in tt.children:
        if isinstance(t, bs4.element.Tag):
            s = t.find('a')
            # print(s)
            # with open('C:/test.txt', 'a') as data:
            #     print(i, file=data)
            #     print(s.get('title'), file=data)
            #     print("https://grs.bupt.edu.cn"+s.get('href'), file=data)
            #     print(file=data)
            # print(s.get('href'))
            if i<10:
                url_new = "https://grs.bupt.edu.cn" + s.get('href')
                random_agent = USER_AGENTS[randint(0, len(USER_AGENTS) - 1)]
                # 蘑菇隧道代理服务器地址
                ip_port = 'secondtransfer.moguproxy.com:9001'

                headers2['Connection'] = 'keep-alive'
                headers2['User-Agent'] = random_agent
                proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}

                while True:  # 一直循环，直到访问站点成功
                    try:
                        # 以下except都是用来捕获当requests请求出现异常时，
                        # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
                        r = requests.get(url_new, headers=headers2, timeout=None, proxies=proxy, verify=False, allow_redirects=False)
                        break
                    except requests.exceptions.ProxyError:
                        print('ProxyError -- please wait 3 seconds')
                        time.sleep(3)
                    except requests.exceptions.ChunkedEncodingError:
                        print('ChunkedEncodingError -- please wait 3 seconds')
                        time.sleep(3)
                    except:
                        print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
                        time.sleep(3)

                # 以下处理返回错误的情况
                while r.status_code != 200:
                    time.sleep(3)
                    r = requests.get(url_new, headers=headers2, timeout=None, proxies=proxy, verify=False, allow_redirects=False)

                # if r.status_code == 302 or r.status_code == 301:
                #     loc = r.headers['Location']
                #     print(loc)
                #     url_f = loc
                #     r = requests.get(url_f, headers=headers2, timeout=None, proxies=proxy, verify=False, allow_redirects=False)
                print(r)
                #获取标题及日期
                title_begin = r.text.find("<ul id=\"title\">")
                title_end = r.text.find("</ul>", title_begin)
                title = r.text[title_begin + 15: title_end]
                date_begin = r.text.find("<ul id=\"date\">")
                date_end = r.text.find("&n", date_begin)
                date = r.text[date_begin + 19: date_end]
                title_new = title + "[" + date + "]"
                
                #上传至数据库
                sql = "INSERT INTO news_YJSY(title, url) VALUES ('" + title_new + "', '" + url_new+"')"
                cursor.execute(sql)
                db.commit()
                headers2['Connection'] = 'false'
                i = i + 1
                time.sleep(10)
    db.close()
schedule.every().day.at("08:00").do(doSth)

while True:
    #doSth()
    schedule.run_pending()
    time.sleep(60)






