# -*- coding: utf-8 -*-
from multiprocessing import Pool # Pool import하기
from requests import get  # to make GET request
import socket
import shutil
import os
import time
import zipfile


start_time = time.time()

# url 다운로드 함수
def download(url, file_name):
    with open(file_name, "wb") as file:   # open in binary mode
        response = get(url)               # get request
        file.write(response.content)      # write to file

# 오늘 날짜 함수
def get_today():
    now = time.localtime()
    a = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    s = a + "\\"
    return s

# 폴더 생성 함수
def createFile(createPath):
    if not os.path.isdir(createPath):
        os.mkdir(createPath)
        return '경로에 폴더를 생성하였습니다.'
    else:
        return '이미 폴더가 생성되었습니다.'

# 압축폴더 해체 함수
def unzip(source_file, dest_path):
    with zipfile.ZipFile(source_file, 'r') as zf:
        zipInfo = zf.infolist()
        for member in zipInfo:
            try:
                #인코딩
                print(member.filename.encode('cp437').decode('euc-kr', 'ignore'))
                member.filename = member.filename.encode('cp437').decode('euc-kr', 'ignore')
                zf.extract(member, dest_path)
            except:
                print(source_file)
                raise Exception('what?!')

# 기본경로 % 주의 % path 경로 맨뒤에 꼭 "\\" 추가해주어야 한다.
download_url = "https://datasets.imdbws.com/" # DataSet 파일을 받을 url 경로
user_name = socket.gethostname() # 컴퓨터 user 이름
desktop_path = "C:\\Users\\" + user_name + "\\Desktop\\"
project_path = desktop_path + "git\\take_a_look_Dev\\Project\\Python_DB\\"
dataset_path = desktop_path + "Dataset\\"

# 날짜 함수 -> 변수 대입
today_dir = get_today()

# DB에 테이블을 만들 dataset list
dataset = ["title.basics.tsv.gz", "name.basics.tsv.gz", "title.crew.tsv.gz",
           "title.principals.tsv.gz", "title.ratings.tsv.gz"]

datasetzip = ["basic_titles.zip", "basic_names.zip", "crew.zip",
               "principals.zip", "ratings.zip"]

datasettsv = ["basic_titles.tsv", "basic_names.tsv", "crew.tsv",
               "principals.tsv", "ratings.tsv"]

# Dataset 다운로드
if __name__ == '__main__':
    for i in range(5):
        url = download_url + dataset[i] # 다운받기
        download(url,datasetzip[i])
        print(str(i+1), datasetzip[i] + "을 생성했습니다.")
    print("모든 Dataset zip 파일을 다운받았습니다.")

# 오늘 날짜로 폴더 생성
dataset_daypath = dataset_path + today_dir + "\\"
print(createFile(dataset_path) + "\n" + createFile(dataset_daypath))

# 프로젝트 폴더에 다운받은 알집을 Dataset폴더로 옮김
for i in range(5):
    shutil.move(project_path + datasetzip[i], dataset_daypath + datasetzip[i])
    print(datasetzip[i] + " 파일을", dataset_path + " 폴더로 옮겼습니다.", i)


pool = Pool(processes=5)
pool.map(__name__) # 실행문/함수 입력
print("--- Multiprocessing %s seconds ---" % (round(time.time() - start_time, 2)) )

# print("재 압축을 완료했으면 q를 입력해주세요..")
# while True:
#     pressedKey = input()
#     if pressedKey == 'q':
#         break
#     else:
#        print ("'q' 를 입력해주세요.")
#
# for i in range(5):
#     unzip(dataset_path + today_dir + datasetzip[i],
#           dataset_path + today_dir)
#     print(today_dir, str(i + 1), datasetzip[i] + " 압축 해제")

