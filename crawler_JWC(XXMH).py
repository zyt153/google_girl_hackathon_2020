# 需要下载 Chromedriver， 版本号需和本地Chrome浏览器版本匹配， 并安装到Chrome路径下以及python运行程序路径下面
# 还需改进的地方是:模拟自动登录时需要打开浏览器页面

import sqlite3
import requests
import re
from bs4 import BeautifulSoup
import bs4
from random import randint
import time
import schedule
from  selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



def doSth():
    # 设置代理、头部、以及随机更换的用户代理，进而反爬虫
    appKey = "R0owSVhtV1pNaVBhZFNDUDpOVGhydzdyWEJqRnhsemNI"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'webvpn.bupt.edu.cn',
        'Referer': 'https://webvpn.bupt.edu.cn/http/77726476706e69737468656265737421fdee0f9e32207c1e7b0c9ce29b5b/index.portal',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    }
    headers2 = {
        'Proxy-Authorization': 'Basic ' + appKey,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'webvpn.bupt.edu.cn',
        'Referer': 'https://webvpn.bupt.edu.cn/http/77726476706e69737468656265737421fdee0f9e32207c1e7b0c9ce29b5b/index.portal',
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

    # 利用selenium自动登录，进入信息门户后返回有效cookie
    #response = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver')
    response = webdriver.Chrome()
    response.get( 'https:/webvpn.bupt.edu.cn/login')
    response.find_element_by_name('username').send_keys('**********')
    response.find_element_by_name('password').send_keys('******')
    response.find_element_by_class_name('el-button-login').click()

    response.implicitly_wait(10)
    # 若账号已经登录，网站会弹出是否要踢掉继续登录，因此需要判断是否有弹窗弹出
    from selenium.common.exceptions import NoSuchElementException
    try:
        element = response.find_element_by_id('layui-layer1')
    except NoSuchElementException: # 没有弹出
        pass
    else:                          # 弹出
        response.find_element_by_xpath("//a[@class='layui-layer-btn0']").click()

    # 登录后进入新网站，需要将respense对象指向新窗口
    response.implicitly_wait(10)
    response.switch_to_window(response.window_handles[-1])

    # 点击信息门户按钮
    element2 = response.find_element_by_class_name('vpn-content-block-panel__content').click()

    # 信息门户登录界面，填写用户名和密码
    response.implicitly_wait(10)
    response.switch_to_window(response.window_handles[-1])
    response.find_element_by_name('username').send_keys('**********')
    response.find_element_by_name('password').send_keys('******')
    response.find_element_by_xpath("//input[@type='submit']").click()

    # 信息门户界面，提取Cookie
    response.implicitly_wait(10)
    response.switch_to_window(response.window_handles[-1])
    webCookies = response.get_cookies()

    # 关掉界面
    response.close()

    # 将获取的cookie转为字典，得到正确的cookie
    webVpncookies = {}
    for item in webCookies:
        webVpncookies[item['name']] = item['value']
    cookies = {'refresh': '1'}
    cookies.update(webVpncookies)
    print(cookies)

    # 打开信息门户最新通知的网址
    url = 'https://webvpn.bupt.edu.cn/http/77726476706e69737468656265737421fdee0f9e32207c1e7b0c9ce29b5b/index.portal?.pn=p1778'
    response2 = requests.get(url, headers=headers, cookies=cookies)  #发出请求
    # print(response2.status_code) # 打印http请求的状态码，返回200代表请求成功
    # print(response2.text)

    # 利用 BeautifulSoup 提取网站信息
    soup = BeautifulSoup(response2.text, 'lxml')
    i = 1 # 记录提取的通知数量，并按照"i.txt"形式存储下来

    #连接并更新数据库
    db = sqlite3.connect('test.db' )
    cursor = db.cursor()
    #cursor.execute('create table news_JWC(title varchar(200) primary key,url varchar(200))')
    cursor.execute('delete from news_JWC')
    
    # 查找通知条目所在的父类标签
    for t in soup.find('ul', class_="newslist list-unstyled").children:
        # 判断是否为有效标签
        if isinstance(t, bs4.element.Tag):
            # 通知在<a>......</a>里
            s = t.find('a')

            # 将链接以及名称存储在文件里
            file = 'test.txt'
            with open(file, 'a', encoding="utf-8") as data:
                data.write(str(i))
                data.write('\n')
                data.write(s.string)
                data.write('\n')
                data.write('https://webvpn.bupt.edu.cn/http/77726476706e69737468656265737421fdee0f9e32207c1e7b0c9ce29b5b/')
                data.write(s.get('href'))
                data.write('\n')

            # 每个通知具体的目录存放在 href属性里
            print(s.get('href'))

            # 提取十条最新通知
            if i<11:
                url_new = "https://webvpn.bupt.edu.cn/http/77726476706e69737468656265737421fdee0f9e32207c1e7b0c9ce29b5b/" + s.get('href')

                headers2['Connection'] = 'keep-alive'
                # 随机设置请求头的用户代理
                random_agent = USER_AGENTS[randint(0, len(USER_AGENTS) - 1)]
                headers2['User-Agent'] = random_agent

                # ip代理服务器地址
                ip_port = 'secondtransfer.moguproxy.com:9001'
                proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}

                r = requests.get(url_new, headers=headers2, cookies=cookies,timeout=None, proxies=proxy, verify=False, allow_redirects=False)
                #print(r)
                while r.status_code == 502:
                    time.sleep(10)
                    r = requests.get(url_new, headers=headers2, cookies=cookies, timeout=None, proxies=proxy,
                                     verify=False, allow_redirects=False)

                if r.status_code == 302 or r.status_code == 301:
                    loc = r.headers['Location']
                    print(loc)
                    url_f = url_new + loc
                    r = requests.get(url_f, headers=headers2, timeout=None, proxies=proxy, verify=False, allow_redirects=False)

                '''#创建"i.txt"文件
                i_str = str(i)
                filename = i_str + '.txt'

                # while open the file, let the file decode in utf-8
                f = open(filename, 'w', encoding="utf-8")
                f.write(r.text)
                f.close'''

                r.encoding = 'utf-8'
                print(r)

                #获取标题及日期
                title_begin = r.text.find("<h1 class")
                title_end = r.text.find("</h1>", title_begin)
                title = r.text[title_begin + 24: title_end]
                date_begin = r.text.find("发布时间")
                date_end = r.text.find("</span>", date_begin)
                date = r.text[date_begin + 6: date_end-5]
                title_new = title + "[" + date + "]"
                
                #上传至数据库
                sql = "INSERT INTO news_JWC(title, url) VALUES ('" + title_new + "', '" + url_new+"')"
                cursor.execute(sql)
                db.commit()        

                # 断开新闻通知的连接，并休息50s，防止反爬虫
                headers2['Connection'] = 'false'
                time.sleep(10)
            i = i+1
    db.close()
schedule.every().day.at("08:00").do(doSth)

while True:
    schedule.run_pending()
    #doSth()
    time.sleep(60)






