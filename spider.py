from bs4 import BeautifulSoup   #网页解析获取数据
import re   #正则表达式进行文字匹配
import urllib.request , urllib.error , requests   #网页请求
import xlwt #进行Excel操作
import sqlite3  #进行sqlite数据库操作

# 主函数
def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist=GetData(baseurl)
    # 3.保存数据到Excel
    # savepath = "./豆瓣TOP250.xls"
    # SaveData(datalist,savepath)

    # 4. 保存数据到数据库
    dbpath="./movies.db"
    SaveData2DB(datalist,dbpath)

#详情链接
findlink=re.compile(r'<a href="(.*?)">')    #创建正则表达式对象，表示规则
#影片图片
findsrc=re.compile(r'<img.*src="(.*?)"',re.S)   #re.S让换行符包含在.匹配符其中
#影片名字
findtitle=re.compile(r'<span class="title">(.*?)</span>')
#影片评分
findrating=re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
#影片评价人数
findjudge=re.compile(r'<span>(\d*?)人评价</span>') 
#影片概况
findinq=re.compile(r'<span class="inq">(.*?)</span>')
#影片相关内容
findbd=re.compile(r'<p class="">(.*?)</p>',re.S)

def GetData(baseurl):
    datalist=[]
    for i in range(0,10):
        url = baseurl + str(i*25)   # 调用获取页面信息函数10次
        html =AskURL(url)
        # 2.边爬取边解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"): #查找符合要求的字符串形成列表，
            data = []   #保存一部影片所有信息
            item=str(item)
            
            #影片详情页链接
            link=re.findall(findlink,item)[0]   #使用re库查找指定字符串
            data.append(link)                   #添加链接

            #影片图片
            imgsrc=re.findall(findsrc,item)[0]
            data.append(imgsrc)                 #添加图片

            #影片名字
            titles=re.findall(findtitle,item)   #片名可能只有中文名没有外文名
            if (len(titles)==2):
                data.append(titles[0])  #添加中文名
                data.append(titles[1].replace("/",""))  #添加外文名
            else:
                data.append(titles[0])
                data.append("")        #留空
            
            #影片评分
            rating=re.findall(findrating,item)[0]
            data.append(rating)                     #添加评分

            #影片评价人数
            judgenum=re.findall(findjudge,item)[0]
            data.append(judgenum)                     #添加评分

            #影片概况
            inq=re.findall(findinq,item)
            if(len(inq)!=0):
                inq=inq[0].replace("。","")    #去掉句号
                data.append(inq)                #添加概况
            else:
                data.append("")                 #留空
            
            #影片相关内容
            bd=re.findall(findbd,item)[0]
            bd=re.sub("<br(\s+)?/>(\s+)?","",bd)
            bd=re.sub("/","",bd)    #去掉 /
            data.append(bd.strip()) #去掉空格，并添加进data

            datalist.append(data)
    
    # print(datalist)

    return datalist

#保存数据
def SaveData(datalist,savepath):

    workbook=xlwt.Workbook(encoding="utf-8")    #创建workbook对象
    worksheet=workbook.add_sheet("豆瓣TOP250")      #创建工作表取名sheet1
    
    col=("电影详情链接","图片链接","影片中文名","影片外文名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        worksheet.write(0,i,col[i])     #添加表头
    for i in range(0,250):
        # print("第%d条"%i)
        data=datalist[i]
        for j in range(0,8):
            worksheet.write(i+1,j,data[j])
    workbook.save(savepath)                #保存数据表取名为student.xls

#得到一个指定url的内容
def AskURL(url):
    headers={   #模拟浏览器头部信息，向豆瓣发送请求
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
    }
    request = urllib.request.Request(url=url,headers=headers)
    try:
        response =urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

def init_db(dbpath):
    sql='''
        create table movies250
        (id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        instroduction text,
        info text)
    '''
    conn=sqlite3.connect(dbpath)
    cursor=conn.cursor()    #获取游标
    cursor.execute(sql)     #执行SQL语句：创建数据表
    conn.commit()           #事务提交：让操作生效
    cursor.close()          #关闭游标
    conn.close()            #关闭连接 

def SaveData2DB(datalist,dbpath):
    init_db(dbpath)
    conn=sqlite3.connect(dbpath)
    cursor=conn.cursor()    #获取游标

    for data in datalist:
        for index in range(len(data)):
            if index ==4 or index==5:
                continue
            data[index]='"'+data[index]+'"'         # sql语句中的字符串添加 " " 
        sql = '''
        insert into movies250(info_link,pic_link,cname,ename,score,rated,instroduction,info)
        values (%s)
        '''%",".join(data)
        # print(data)
        # print("%s"%",".join(data))
        # print(sql)
        cursor.execute(sql)     #执行SQL语句：创建数据表
        conn.commit()           #事务提交：让操作生效

    cursor.close()          #关闭游标
    conn.close()            #关闭连接 


if __name__ == "__main__":
    main()
    