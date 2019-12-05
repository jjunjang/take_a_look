# -*- coding: utf-8 -*-
import pymysql
import socket
import time
import os
import sys

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

# 날짜 함수 -> 변수 대입
print("\n# Dataset폴더 이름형식 Ex) 2019-09-27")
print("# 오늘 날짜로 입력하려면 'y'를 입력하세요.\n")
D_input = str(input("# Dataset을 읽을날짜를 입력해주세요. : "))

# 컴퓨터 user 이름
user_name = socket.gethostname()
dataset_path = "C:/Users/" + user_name + "/Desktop/Dataset/"

datasetTSV = ["basic_titles.tsv", "crew.tsv", "ratings.tsv",
               "basic_names.tsv", "principals.tsv", "emotion.tsv"]

# 리스트 초기화
DataSet = [0]*6
datasetName = [0]*6
datasetLoad = [0]*6
DropResult = [0]*6

def CheckFolder(D_input):
    if (D_input == "y"):
        today_dir = get_today()
    else:
        today_dir = D_input
        if not os.path.isdir(dataset_path + today_dir):
            print ("입력한 날짜폴더가 없습니다.")
    return today_dir

def DatasetUpload():
    # Block 1 start
    print("\nBlock 1 start")
    start_time = time.time()
    print(time.strftime("[%y-%m-%d] %X", time.localtime()))  # 현재시간 출력

    for i in range(len(datasetTSV)):
        input_time_start = time.time()
        ds = datasetTSV[i]
        print("\n# [" + str(i+1), ds + "] Load")
        datasetName[i] = ds[:-4]
        # sql
        datasetLoad = """
                LOAD DATA LOCAL INFILE     '""" + dataset_path + CheckFolder(D_input) + "/" + datasetTSV[i] + """'
                INTO TABLE                 """ + datasetName[i] + """
                CHARACTER SET 			   utf8
                COLUMNS TERMINATED BY      '\t'
                LINES TERMINATED BY        '\r\n'
                IGNORE                     1 LINES;
            """
        DataSet[i] = str(datasetLoad)


        # Dataset Upload
        print("\n# [" + datasetName[i] + "] input start")
        sql = DataSet[i]
        cursor.execute(sql)
        connect.commit()
        print(sql)
        print("ㅡㅡㅡ #Commit ㅡㅡㅡ\n")
        # input time
        input_time = time.time()
        print(time.strftime("[%y-%m-%d] %X", time.localtime()))  # 현재시간 출력
        print("[" + datasetName[i] + "] 소요시간 : %s초" \
              %(round(input_time - input_time_start, 1)))


    # Block 1 end
    print("\nBlock 1 end")
    end_time = time.time()
    print(time.strftime("[%y-%m-%d] %X", time.localtime())) # 현재시간 출력

    # 소요시간
    print("소요시간 : %s초" %round(end_time - start_time, 1))
    print("\n")


Dtable = ["basic_titles", "basic_titles", "basic_titles", "basic_titles", "basic_names", "basic_names"]
Dcolumn = ["originalTitle", "isAdult", "endYear", "runtimeMinutes", "primaryProfession", "knownForTitles"]

# Table drop Column (6개)
print("\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")

def DropTable():
    for i in range(len(DropResult)):
        drop_time_start = time.time()
        # sql
        DropColumn = """
                ALTER TABLE """ + Dtable[i] + """
                DROP COLUMN """ + Dcolumn[i] + """
            """
        DropResult[i] = str(DropColumn)

        # Drop the table row
        print("# " + str(i+1) + " [" + Dtable[i] + "] ALTER table, [" + Dcolumn[i] + "] DROP column start")
        sql = DropResult[i]
        cursor.execute(sql)
        connect.commit()

        print("ㅡㅡㅡ #Commit ㅡㅡㅡ\n")
        # drop time
        drop_time = time.time()
        print(time.strftime("[%y-%m-%d] %X", time.localtime()))  # 현재시간 출력
        print("[" + Dtable[i] + " Table " + Dcolumn[i] + " column " + "] 소요시간 : %s초" \
              %(round(drop_time - drop_time_start, 1)))
        print("\n\n")

DatasetUpload()
DropTable()

# processing end
total_end = time.time()
total_end_time = time.strftime("[%y-%m-%d] %X", time.localtime())

# print processing time
print("%s ~ %s, 총 소요시간 : %s초" \
    %(total_start_time, total_end_time, round(total_end - total_start, 1)))

# SQL SERVER disconnect
connect.close()