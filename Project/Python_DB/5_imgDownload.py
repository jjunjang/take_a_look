# -*- coding: utf-8 -*-
from multiprocessing import Pool # Pool import하기
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
import socket
import pymysql
import urllib.request
import requests
import json
import re

# 스크립트 시작
total_start = time.time()
total_start_time = time.strftime("[%y-%m-%d] %X", time.localtime())

# Local DB
# connect = pymysql.connect(host='localhost',
#                           user='root', password='han1280', db='takealook', charset='utf8', local_infile=1)
# RDS SERVER DB
connect = pymysql.connect(host='takealook.cjdwnzzk2agh.ap-northeast-2.rds.amazonaws.com',
                          user='tal_admin', password='take1234', db='takealook', charset='utf8', local_infile=1)

cursor = connect.cursor(pymysql.cursors.DictCursor)

# 컴퓨터 user 이름, 파일이 저장될 디렉토리
user_name = socket.gethostname()
Loc = "C:\\Users\\" + user_name + "\\Desktop\\Dataset\\img\\"
LocSum = "C:\\Users\\" + user_name + "\\Desktop\\Dataset\\imgSum\\"

# 네이버 검색 Open API 사용 요청시 얻게되는 정보를 입력합니다
naver_client_id = "i2FXVweBP9KWlucnK6g5"
naver_client_secret = ""

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def searchByTitle(title):
    myurl = 'https://openapi.naver.com/v1/search/movie.json?display=2&query=' + quote(title)
    request = urllib.request.Request(myurl)
    request.add_header("X-Naver-Client-Id", naver_client_id)
    request.add_header("X-Naver-Client-Secret", naver_client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        d = json.loads(response_body.decode('utf-8'))
        if (len(d['items']) > 0):
            return d['items']
        else:
            return None

    else:
        print("Error Code:" + rescode)

# 검색 결과가 없으면 액박이미지를 다운
def getInfoFromNaver(searchTitle):
    items = searchByTitle(searchTitle)

    if (items != None):
        findItemByInput(items)
    else:
        X = "https://ssl.pstatic.net/static/movie/2012/06/dft_img203x290.png"
        urllib.request.urlretrieve(X, "%s%s.jpg" % (Loc, tconst))
        print("["+ tconst + "] "+ searchTitle + "에 대한 검색결과가 없습니다.\n")

def imgSrc(url):
    with urllib.request.urlopen(url) as response:
        source = response.read()
        soup = BeautifulSoup(source, 'html.parser')

        if (soup.find("div", id=True) is not None):
            img = soup.find("img", id="targetImage")
            img_src = img.get("src")
            return img_src
        else:
                        # 영화를 준비중 입니다. // 액박
            naverBig = "https://ssl.pstatic.net/static/movie/2012/06/dft_img203x290.png"
            return naverBig

def get_soup(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    return soup



def findItemByInput(items):
    for index, item in enumerate(items):
        navertitle = cleanhtml(item['title'])
        naversubtitle = cleanhtml(item['subtitle'])
        naverpubdate = cleanhtml(item['pubDate'])
        naverdirector = cleanhtml(item['director'])
        naveractor = cleanhtml(item['actor'])
        naverlink = cleanhtml(item['link'])
        naverimage = cleanhtml(item['image'])

        navertitle = navertitle.replace(" ", "")
        navertitle = navertitle.replace("-", ",")
        navertitle = navertitle.replace(":", ",")
        navertitle = navertitle.replace("!", "")

        naversubtitle = naversubtitle.replace("!", "")
        naversubtitle = naversubtitle.replace(":", "")

        primaryName = primaryTitle.replace("?", "")
        primaryName = primaryName.replace("/", "")
        primaryName = primaryName.replace("*", "")

        # 네이버가 다루는 영화 고유 ID를 얻어 옵니다다
        naverid = re.split("code=", naverlink)[1]

        naverUri = "https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode="
        naverBig = naverUri + naverid

        print("[" + str(count) + "] (" + naverid + ") # " + navertitle + " # 출시년도 " + naverpubdate + " # 서브 제목 : " + naversubtitle)

        if (primaryTitle == naversubtitle):
            # urllib.request.urlretrieve(imgSrc(naverBig), Loc + tconst + "_" + primaryName + ".jpg")
            urllib.request.urlretrieve(imgSrc(naverBig), "%s%s.jpg" % (Loc, tconst))
            # print(imgSrc(naverBig)+"\n")
        else:
            # X = "https://ssl.pstatic.net/static/movie/2012/06/dft_img203x290.png"
            # urllib.request.urlretrieve(X, "%s%s_%s.jpg"%(Loc, tconst, primaryName))
            urllib.request.urlretrieve(imgSrc(naverBig), "%s%s.jpg" % (Loc, tconst))
            print("NULL\n")
            # print(imgSrc(naverBig))


if __name__ =='__main__':
    # sql실행
    sql = "SELECT tconst, primaryTitle, startYear FROM basic_titles"
    cursor.execute(sql)
    rows = cursor.fetchall()
    count = 1

    for row in rows:
        # row 출력 : {'tconst' : 'tt000000', 'primaryTitle' : 'ABC'}
        tconst = row['tconst']
        primaryTitle = row['primaryTitle']
        startYear = row['startYear']
        # print(row['tconst'], row['primaryTitle'], row['startYear'])
        getInfoFromNaver(primaryTitle)
        count += 1

    connect.close()

start_time = time.time()
pool = Pool(processes=5)
pool.map(__name__) # 실행문/함수 입력

# processing end
total_end = time.time()
total_end_time = time.strftime("[%y-%m-%d] %X", time.localtime())

# print processing time
print("%s ~ %s, 총 소요시간 : %s초" \
      % (total_start_time, total_end_time, round(total_end - total_start, 1)))