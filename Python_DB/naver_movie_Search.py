# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import json
import re
import requests

# 네이버 검색 Open API 사용 요청시 얻게되는 정보를 입력합니다
naver_client_id = "i2FXVweBP9KWlucnK6g5"
naver_client_secret = "rvzS0ngsDd"


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def searchByTitle(title):
    myurl = 'https://openapi.naver.com/v1/search/movie.json?display=100&query=' + quote(title)
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


def findItemByInput(items):
    for index, item in enumerate(items):
        navertitle = cleanhtml(item['title'])
        naversubtitle = cleanhtml(item['subtitle'])
        naverpubdate = cleanhtml(item['pubDate'])
        naveractor = cleanhtml(item['actor'])
        naverlink = cleanhtml(item['link'])

        navertitle1 = navertitle.replace(" ", "")
        navertitle1 = navertitle1.replace("-", ",")
        navertitle1 = navertitle1.replace(":", ",")

        # 네이버가 다루는 영화 고유 ID를 얻어 옵니다다
        naverid = re.split("code=", naverlink)[1]

        naverUri = "https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode="
        naverBig = naverUri + naverid

        print(index, navertitle, naverpubdate, naversubtitle, naverpubdate)
        print(naverBig)

        Loc = "C:/Users/JJunJang/Desktop/take_a_look/Python_DB/"
        FileName = "File1"
        urllib.request.urlretrieve(naverBig, Loc + FileName + ".png")
                                # (다운로드할 이미지 Url, 저장할 파일경로 / 파일명)

def getInfoFromNaver(searchTitle):
    items = searchByTitle(searchTitle)

    if (items != None):
        findItemByInput(items)
    else:
        print("No result")


def get_soup(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    return soup

getInfoFromNaver(u"사랑")