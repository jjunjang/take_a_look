# -*- coding: utf-8 -*-
import pymysql
import socket
import time
import os

# 스크립트 시작
total_start = time.time()
total_start_time = time.strftime("[%y-%m-%d] %X", time.localtime())


# Local DB
connect = pymysql.connect(host='localhost',
                          user='root', password='han1280', db='takealook', charset='utf8', local_infile=1)
# RDS SERVER DB
# connect = pymysql.connect(host='takealook.cjdwnzzk2agh.ap-northeast-2.rds.amazonaws.com',
#                           user='tal_admin', password='take1234', db='takealook', charset='utf8', local_infile=1)

cursor = connect.cursor(pymysql.cursors.DictCursor)
    
# 오늘 날짜 함수
def get_today():
    now = time.localtime()
    today = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    today_ = today + "/"
    return today_

# 컴퓨터 user 이름, 파일이 저장될 디렉토리
user_name = socket.gethostname()
Loc = "C:\\Users\\" + user_name + "\\Desktop\\Dataset\\tsv\\"
UrlS3 = "https://takealookdb.s3.ap-northeast-2.amazonaws.com/"

def sql():
    # sql실행
    sql = "SELECT tconst FROM basic_titles"
    cursor.execute(sql)
    rows = cursor.fetchall()
    count = 1

    f = open(Loc + "tconstUrl.tsv", 'w', encoding='utf8')
    f.write("tconst" + "\t" + "imgUrl" + "\n")

    for row in rows:
        f = open(Loc + "tconstUrl.tsv", 'a', encoding='utf8')
        tconst = row['tconst']
        tconstUrl = UrlS3 + tconst + ".jpg"
        f.write(tconst + "\t" + tconstUrl + "\n")
        print("[" + str(count) + "]" + tconstUrl)
        count += 1
        f.close()

    print("[Clear]")
    f.close()

def upload():
    tsv = """
        LOAD DATA LOCAL INFILE     'C:/Users/JJunJang/Desktop/Dataset/tsv/tconstUrl.tsv'
        INTO TABLE					url
        CHARACTER SET 			   	utf8
        COLUMNS TERMINATED BY      '\t'
        LINES TERMINATED BY        '\r\n'
        IGNORE                     1 LINES;
        """

    # Dataset Upload
    sql = tsv
    cursor.execute(sql)
    connect.commit()
    print(sql)
    print("ㅡㅡㅡ #Commit ㅡㅡㅡ\n")



sql()
upload()
connect.close()