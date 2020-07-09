# coding: utf-8
# schedule控制开始运行时间

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
    # 图书网站的请求头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'pgv_pvi=5512413184',
        'Host': 'lib.bupt.edu.cn',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'cross-site',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    }

    # 公告的请求头
    appKey = "R0owSVhtV1pNaVBhZFNDUDpOVGhydzdyWEJqRnhsemNI"
    headers2 = {
        'Proxy-Authorization': 'Basic ' + appKey,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'pgv_pvi=5512413184',
        'Host': 'lib.bupt.edu.cn',
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

    url = 'https://lib.bupt.edu.cn/index.html'
    response = requests.post(url, headers=headers)
    response.encoding='utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    i = 1

    # 获取公告的具体网址
    tt = soup.find('table', border="0", class_="mytable")

    #清空保存通知条目的文件
    try:
        f = open('WebSite.txt', "r+")
    except:
        pass
    else:
        f.seek(0)
        f.truncate()  # 清空文件

    #连接并更新数据库
    db = sqlite3.connect('test.db' )
    cursor = db.cursor()
    #cursor.execute('create table news_TSG(title varchar(200) primary key,url varchar(200))')
    cursor.execute('delete from news_TSG')
    
    for t in tt.children:
        if isinstance(t, bs4.element.Tag):
            s = t.find('td', style="font-size: 12px;width:70%")

            # 将公告的网址写入文本中，如果不存在这个文本，就新建一个，否则直接在文本的后面添加内容
            with open('WebSite.txt', 'a') as data:
                data.write(str(i)+'\n')
                data.write(s.string +'\n')
                data.write('https://lib.bupt.edu.cn'+s.find('a').get('href')+'\n')


            url_new = "https://lib.bupt.edu.cn" + s.find('a').get('href')

            headers2['Connection'] = 'keep-alive'
            random_agent = USER_AGENTS[randint(0, len(USER_AGENTS) - 1)]
            headers2['User-Agent'] = random_agent
            # 蘑菇隧道代理服务器地址
            ip_port = 'secondtransfer.moguproxy.com:9001'
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

            # 以下处理http返回错误的情况
            while r.status_code != 200:
                time.sleep(3)
                r = requests.get(url_new, headers=headers2, timeout=None, proxies=proxy, verify=False, allow_redirects=False)

            # print((r.status_code))

            # 判断返回的状态码
            if r.status_code == 502:
                time.sleep(10)
                r = requests.get(url_new, headers=headers2, timeout=None, proxies=proxy, verify=False,allow_redirects=False)

            r.encoding = 'utf-8'
            print(r)
            '''filename = str(i) + '.txt'
            f = open(filename, 'w', encoding="utf-8")
            f.write(r.text)
            f.close'''
            #获取标题及日期
            title_begin = r.text.find("<title>")
            title_end = r.text.find("</title>", title_begin)
            title = r.text[title_begin + 7: title_end - 10]
            date_begin = r.text.find(">2020")
            date_end = r.text.find("<", date_begin)
            date = r.text[date_begin + 1: date_end]
            title_new = title + "[" + date + "]"
                
            #上传至数据库
            sql = "INSERT INTO news_TSG(title, url) VALUES ('" + title_new + "', '" + url_new+"')"
            cursor.execute(sql)
            db.commit()        
    
            headers2['Connection'] = 'false'
            time.sleep(20)
            i = i+1
    db.close()
schedule.every().day.at("08:00").do(doSth)

while True:
    #doSth()
    schedule.run_pending()
    time.sleep(60)




