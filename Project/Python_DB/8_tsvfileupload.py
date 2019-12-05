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

tsvfile = ["titleKor.tsv"]
tabletsv = ["basic_titles"]

# 리스트 초기화
DataSet = [0]*6

def DatasetUpload():
    # Block 1 start
    print("\nBlock 1 start")
    start_time = time.time()
    print(time.strftime("[%y-%m-%d] %X", time.localtime()))  # 현재시간 출력

    for i in range(len(tsvfile)):
        input_time_start = time.time()
        ds = tsvfile[i]
        print("\n# [" + str(i+1), ds + "] Load")
        # sql
        datasetLoad = """
                LOAD DATA LOCAL INFILE     '""" + Loc + tsvfile[i] + """'
                INTO TABLE                 """ + tabletsv[i] + """
                CHARACTER SET 			   utf8
                COLUMNS TERMINATED BY      '\t'
                LINES TERMINATED BY        '\n'
                IGNORE                     1 LINES;
            """
        DataSet[i] = str(datasetLoad)


        # Dataset Upload
        print("\n# [" + tsvfile[i] + "] input start")
        sql = DataSet[i]
        cursor.execute(sql)
        connect.commit()
        print(sql)
        print("ㅡㅡㅡ #Commit ㅡㅡㅡ\n")
        # input time
        input_time = time.time()
        print(time.strftime("[%y-%m-%d] %X", time.localtime()))  # 현재시간 출력
        print("[" + tsvfile[i] + "] 소요시간 : %s초" \
              %(round(input_time - input_time_start, 1)))


    # Block 1 end
    print("\nBlock 1 end")
    end_time = time.time()
    print(time.strftime("[%y-%m-%d] %X", time.localtime())) # 현재시간 출력

    # 소요시간
    print("소요시간 : %s초" %round(end_time - start_time, 1))
    print("\n")


DatasetUpload()

# processing end
total_end = time.time()
total_end_time = time.strftime("[%y-%m-%d] %X", time.localtime())

# print processing time
print("%s ~ %s, 총 소요시간 : %s초" \
    %(total_start_time, total_end_time, round(total_end - total_start, 1)))

# SQL SERVER disconnect
connect.close()