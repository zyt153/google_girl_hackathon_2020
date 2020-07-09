#!/usr/bin/python3.5
# -*- coding: UTF-8 -*-
#导入数据库模块
import sqlite3
#导入Flask框架，这个框架可以快捷地实现了一个WSGI应用 
from flask import Flask
#默认情况下，flask在程序文件夹中的templates子文件夹中寻找模块
from flask import render_template
#导入前台请求的request模块
from flask import request, redirect  
from werkzeug.utils import secure_filename
import traceback
import os
import cv2

#传递根目录
app = Flask(__name__)

#默认路径访问登录页面
@app.route('/')
def login():
    return render_template('login.html')

#默认路径访问注册页面
@app.route('/regist')
def regist():
    return render_template('regist.html')

#设置响应头
def Response_headers(content):    
    resp = Response(content)    
    resp.headers['Access-Control-Allow-Origin'] = '*'    
    return resp 

#获取注册请求及处理
@app.route('/registuser')
def getRigistRequest():
#把用户名和密码注册到数据库中

    #连接数据库,此前在数据库中创建数据库TESTDB
    db = sqlite3.connect('test.db' )
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    #执行一条SQL语句：创建user表
    #cursor.execute('create table user(user varchar(20) primary key,password varchar(20))')
    # SQL 插入语句
    sql = "INSERT INTO user(user, password) VALUES ("+request.args.get('user')+", "+request.args.get('password')+")"
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
         #注册成功之后跳转到登录页面
        return render_template('login.html') 
    except:
        #抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        return '注册失败'
    # 关闭数据库连接
    db.close()

#获取登录参数及处理
@app.route('/login')
def getLoginRequest():
    #查询用户名及密码是否匹配及存在
    #连接数据库,此前在数据库中创建数据库TESTDB
    db = sqlite3.connect('test.db' )
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    # SQL 查询语句
    sql = "select * from user where user="+request.args.get('user')+" and password="+request.args.get('password')+""
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results))
        if len(results)==1:
            return redirect('/welcome')
        else:
            return '用户名或密码不正确'
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
    # 关闭数据库连接
    db.close()

#首页
@app.route('/welcome')
def welcome():
    news = []
    news_dic = ['title1', 'url1','title2', 'url2','title3', 'url3','title4', 'url4',
    'title5', 'url5','title6', 'url6','title7', 'url7','title8', 'url8',
    'title9', 'url9','title10', 'url10','title11', 'url11','title12', 'url12',
    'title13', 'url13','title14', 'url14','title15', 'url15','title16', 'url16',
    'title17', 'url17','title18', 'url18','title19', 'url19','title20', 'url20',
    'title21', 'url21','title22', 'url22','title23', 'url23','title24', 'url24',]

    for i in range(8):
        db = sqlite3.connect('test.db' )
        cursor = db.cursor()
        sql = "select * from news_JWC where rowid = " + str(i+1)
        cursor.execute(sql)
        news.append(str(cursor.fetchall()[0][0]))
        cursor.execute(sql)
        news.append(str(cursor.fetchall()[0][1]))

    for i in range(8):
        db = sqlite3.connect('test.db' )
        cursor = db.cursor()
        sql = "select * from news_YJSY where rowid = " + str(i+1)
        cursor.execute(sql)
        news.append(str(cursor.fetchall()[0][0]))
        cursor.execute(sql)
        news.append(str(cursor.fetchall()[0][1]))

    for i in range(8):
        db = sqlite3.connect('test.db' )
        cursor = db.cursor()
        sql = "select * from news_TSG where rowid = " + str(i+1)
        cursor.execute(sql)
        news.append(str(cursor.fetchall()[0][0]))
        cursor.execute(sql)
        news.append(str(cursor.fetchall()[0][1]))
    
    variable1 = dict(zip(news_dic,news))
    #variable1={"title1": title[0], "url1": url[0]}
    return render_template('首页.html',variable=variable1)

#口罩检测
@app.route('/mask')
def mask():
    return render_template('口罩检测.html')

#口罩检测认错
@app.route('/maskRemove')
def maskRemove():
    return render_template('口罩检测认错.html')

#人流密度
@app.route('/density')
def density():
    #连接数据库
    db = sqlite3.connect('test.db' )
    cursor = db.cursor()
    
    sql = "select num_people from density where location = ' 综合食堂 '"
    cursor.execute(sql)
    zongheshitang = cursor.fetchall()[0][0]

    sql = "select num_people from density where location = ' 教工餐厅 '"
    cursor.execute(sql)
    jiaogongcanting = cursor.fetchall()[0][0]
    
    sql = "select num_people from density where location = ' 学生食堂 '"
    cursor.execute(sql)
    xueshengshitang = cursor.fetchall()[0][0]

    sql = "select num_people from density where location = ' 学苑超市 '"
    cursor.execute(sql)
    xueyuanchaoshi = cursor.fetchall()[0][0]

    sql = "select num_people from density where location = ' 浴室 '"
    cursor.execute(sql)
    zaotang = cursor.fetchall()[0][0]

    sql = "select num_people from density where location = ' 图书馆 '"
    cursor.execute(sql)
    tushuguan = cursor.fetchall()[0][0]

    sql = "select num_people from density where location = ' 主楼 '"
    cursor.execute(sql)
    zhulou = cursor.fetchall()[0][0]

    sql = "select num_people from density where location = ' 教一 '"
    cursor.execute(sql)
    j1 = cursor.fetchall()[0][0]

    sql = "select num_people from density where location = ' 教二 '"
    cursor.execute(sql)
    j2 = cursor.fetchall()[0][0]

    sql = "select num_people from density where location = ' 教三 '"
    cursor.execute(sql)
    j3 = cursor.fetchall()[0][0]

    sql = "select num_people from density where location = ' 教四 '"
    cursor.execute(sql)
    j4 = cursor.fetchall()[0][0]

    db.close()

    variable={"zongheshitang": zongheshitang,
    "jiaogongcanting": jiaogongcanting,
    "xueshengshitang": xueshengshitang,
    "xueyuanchaoshi": xueyuanchaoshi,
    "zaotang": zaotang,
    "tushuguan": tushuguan,
    "zhulou": zhulou,
    "j1": j1,
    "j2": j2,
    "j3": j3,
    "j4": j4
    }
    
    return render_template('人流密度.html',variable=variable)

#每日填报
@app.route('/report')
def report():
    return render_template('每日填报.html')

#每日填报响应
@app.route('/reportuser')
def getReportRequest():
    db = sqlite3.connect('test.db')
    cursor = db.cursor()

    user = request.args.get('user')
    name1 = request.args.get('name1')
    temperature = request.args.get('temperature')
    goOut = request.args.get('goOut')
    where1 = request.args.get('where')
    rout1 = request.args.get('route1')
    time1 = request.args.get('time1')
    rout2 = request.args.get('route2')
    time2 = request.args.get('time2')
    rout3 = request.args.get('route3')
    time3 = request.args.get('time3')
    rout4 = request.args.get('route4')
    time4 = request.args.get('time4')
    rout5 = request.args.get('route5')
    time5 = request.args.get('time5')

    sql = '''INSERT INTO report(studentID, sname,temperature,goOut,where1,track1,time1,track2,time2,track3,time3,track4,time4,track5,time5)\
            VALUES (:_studentID, :_sname,:_temperature,:_goOut,:_where1,:_track1,:_time1,:_track2,:_time2,:_track3,:_time3,:_track4,:_time4,:_track5,:_time5)'''
    try:
        # 执行sql语句
        cursor.execute(sql,{'_studentID':user, '_sname':name1,'_temperature':temperature,'_goOut':goOut,'_where1':where1,'_track1':rout1,'_time1':time1,\
                            '_track2':rout2,'_time2':time2,'_track3':rout2,'_time3':time3,'_track4':rout4,'_time4':time4,'_track5':rout5,'_time5':time5})
        # 提交到数据库执行
        db.commit()
        # 提交成功之后跳转到提交成功页面
        return render_template('reportSuccess.html')
    except:
        # 抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        return render_template('reportFail.html')
    # 关闭数据库连接
    db.close()

if __name__ == '__main__':
    app.run(debug=True)