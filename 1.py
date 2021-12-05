# -*- codeing = utf-8 -*-
# @Time : 2021/11/28 0:55
# @Author: QiuDer
from bs4 import BeautifulSoup       #网页解析，获取数据
import re                           #正则表达式，进行文字匹配
import urllib.response,urllib.error #制定URL，获取网页数据
import xlwt                         #进行excel操作
import sqlite3                      #进行sqlit数据库操作
import urllib.request

def main():
    baseurl ="https://movie.douban.com/top250?start="
    #1.爬取网页
    datalist = getData(baseurl)
    #dbpath = "movie.db"
    #savepath = "豆瓣电影TOP250.xls"
    saveData(datalist,savepath)
    #saveData2db(datalist,dbpath)
findlist = re.compile(r'<a href="(.*?)">')
findsrc = re.compile(r'<img.*?src="(.*?)"',re.S)
findtitle = re.compile(r'<span class="title">(.*)</span>')
findrating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findjudge = re.compile(r'<span>(\d*)人评价</span>')
findinq = re.compile(r'<span class="inq">(.*)</span>')
findbd = re.compile(r'<p class="">(.*?)</p>',re.S)

#1.爬取网页
def getData(baseurl):
    datalist = []
    #逐一解析数据
    for i in range(0, 10):
        url = baseurl + str(i*25)
        html = askurl(url)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            data = []
            item = str(item)

            link = re.findall(findlist,item)[0]#储存链接
            data.append(link)

            src = re.findall(findsrc,item)[0]#储存照片
            data.append(src)

            titles = re.findall(findtitle,item)#储存名字
            if(len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)
                etitle = titles[1].replace("/","")
                etitle = etitle.replace(" ","")
                data.append(etitle)
            else:
                data.append(titles[0])
                data.append(' ')

            rating = re.findall(findrating,item)[0]#储存评分
            data.append(rating)

            num = re.findall(findjudge,item)[0]#储存人数
            data.append(num)

            inq = re.findall(findinq,item)#评价概述
            if len(inq) != 0:
                inq = inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findbd,item)[0]
            bd = re.sub("<br(\s+)?/>(\s+)?"," ",bd)#去br
            bd = re.sub(" ","",bd)
            bd = re.sub("/"," ",bd)
            data.append(bd.strip())#去前后空格
            datalist.append(data)
    return datalist
#获取一个网页的信息
def askurl(url):#"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"}
    request = urllib.request.Request(url,headers=head)#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"
    html = ""
    try :
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"error"):
            print(e.error)
    return html


def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评分人数","概括","相关信息")
    for i in range(0, 8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save(savepath)

# def saveData2db(datalist,dbpath):
#     crea_db(dbpath)
#     conn = sqlite3.connect(dbpath)
#     cur = conn.cursor()
#     for data in datalist:
#         for index in range(len(data)):
#             data[index] ='"'+data[index]+'"'
#         sql = '''
#             insert into movie250(
#             info_link,pic_link,Chinese_name,Foreign_name,score,rated,introduction,info)
#             values(%s)'''%",".join(data)
#         cur.execute(sql)
#         conn.commit()
#     cur.close()
#    conn.close()

# def crea_db(dbpath):
#     sql = '''
#     create table movie250
#     (
#     id integer primary key autoincrement,
#     info_link text,
#     pic_link text,
#     Chinese_name varchar,
#     Foreign_name varchar,
#     score numeric,
#     rated numeric,
#     introduction text,
#     info text
#     )
#     '''
#     conn = sqlite3.connect(dbpath)
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     conn.commit()
#     conn.close()

if __name__ == "__main__":
    main()