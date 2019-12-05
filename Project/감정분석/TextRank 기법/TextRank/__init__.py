# -*- coding: utf-8 -*-
__name__ = 'textrank'
__author__ = 'lovit'
__version__ = '0.1.2'

from .summarizer import KeywordSummarizer
from .summarizer import KeysentenceSummarizer
from konlpy.tag import Komoran
from textrank import KeywordSummarizer

import csv
import re
import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
from collections import Counter

stemmer = nltk.stem.PorterStemmer()         #PoterStemmer 를 이용하여 스테밍
stop_words = set(stopwords.words('english'))  # 불용어 제거용 stopwords
tokenizer = TreebankWordTokenizer()  # 토큰화를 위해


def Input():
    f = open("D:\\Project\\WebCrowling\\tt0387564.tsv", 'r', encoding='utf-8')
    rdr = list(csv.reader(f, delimiter='\t', quoting=3))
    global Star, Id, Title, Content
    Star = []
    Id = []
    Title = []
    Content = []
    f.close()

    # 읽어온 파일을 추가하는 단.
    for line in rdr:
        Star.append(line[0])
        Id.append(line[1])
        Title.append(line[2])
        Content.append(line[3])

    return Star, Id, Title, Content


# 읽어온 Title,Content를 토큰화 / 정제화 뒤, 인덱스화 하는단.
def text_refine():
    Input()
    Title_Result = []
    Content_Result = []
    Difinitive_Title = []
    Difinitive_Content = []
    vocab_Title = Counter()  # 파이썬의 Counter 모듈을 이용하면 단어의 모든 빈도를 쉽게 계산할 수 있습니다.
    vocab_Content = Counter()
    for i in range(len(Content)):
        Title_Token = tokenizer.tokenize(Title[i])  # 타이틀 토큰화
        Content_Token = tokenizer.tokenize(Content[i])  # 컨텐츠 토큰화


        for word in Title_Token:
            word = re.sub('[^a-zA-Z]', '', word)  # 영문자 제외 모두 삭제
            word = word.lower()  # 소문자
            if word not in stop_words:  # 불용어에 포함되어 있지 않은것
                if len(word) > 2:  # 길이가 2자리 이하인것은 제외
                    word = format(stemmer.stem(word))
                    Title_Result.append(word)  # 을 추가.
                    vocab_Title[word] = vocab_Title[word] + 1
        Difinitive_Title.extend(Title_Result)  # 모든 정제작업이 이루워진 배열이 Difinitive 배열

        for word in Content_Token:
            word = re.sub('[^a-zA-Z]', '', word)  # 영문자 제외 모두 삭제
            word = word.lower()  # 소문자
            if word not in stop_words:  # 불용어에 포함되어 있지 않은것
                if len(word) > 2:  # 길이가 2자리 이하인것은 제외
                    Content_Result.append(word)  # 을 추가.
                    vocab_Content[word] = vocab_Content[word] + 1
        Difinitive_Content.extend(Content_Result)
    global T_vocab_sorted, C_vocab_sorted
    T_vocab_sorted = sorted(vocab_Title.items(), key=lambda x: x[1], reverse=True)
    C_vocab_sorted = sorted(vocab_Content.items(), key=lambda x: x[1], reverse=True)
    return Difinitive_Title, Difinitive_Content

komoran = Komoran()

def komoran_tokenize(sent):
    words = komoran.pos(sent, join=True)
    words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
    return words


keyword_extractor = KeywordSummarizer(
    tokenize = komoran_tokenize,
    window = -1,
    verbose = False
)

def komoran_tokenize(sent):
    return komoran.pos(sent, join=True)


title, Content = text_refine()

keyword_extractor = KeywordSummarizer(tokenize = komoran_tokenize, window = -1)
keywords = keyword_extractor.summarize(Content, topk=300)

print(keywords)

