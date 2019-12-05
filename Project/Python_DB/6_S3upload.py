# -*- coding: utf-8 -*-
import boto3
import os
import time
from botocore.exceptions import NoCredentialsError
from multiprocessing import Pool # Pool import하기

# 시작시간
start_time = time.time()
print(time.strftime("[%y-%m-%d] %X", time.localtime())) # 현재시간 출력

ACCESS_KEY = 'AKIAX2R4V25UA7N2724I'
SECRET_KEY = ''
# 업로드할 폴더 경로
path_dir = "C:\\Users\\JJunJang\\Desktop\\Dataset\\img_resize\\"

# s3 파일 업로드 함수
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={"ContentType": "image/jpeg"} )
        # print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

file_name = []

def fileName():
    file_list = os.listdir(path_dir) # Path에 존재하는 tconst 목록 읽기
    file_list.sort() # 파일 이름 순서대로 정렬

    count = 1
    for file_name in file_list:
        # 업로드 할 때 같은이름의 파일이 업로드 되어있는 경우 겹치지 않는다.
        uploaded = upload_to_aws(path_dir + file_name, 'takealookdb', file_name) # 파일경로, S3버킷이름, S3업로드 될 파일이름
        count += 1
        print("[%s] %s"%(count, file_name))
    return uploaded, print("--- uploads %s seconds ---"% (round(time.time() - start_time, 2)) )

if __name__=='__main__':
    start_time = time.time()
    pool = Pool(processes=6) # 6개의 프로세스를 사용합니다.
    pool.map(fileName()) # 실행문/함수 입력
    print("--- Multiprocessing %s seconds ---" % (round(time.time() - start_time, 2)) )

# 업로드 파일 url Example
# https://takealookdb.s3.ap-northeast-2.amazonaws.com/tt0031381.jpg