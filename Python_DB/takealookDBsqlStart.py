# -*- coding: utf-8 -*-
import pymysql
import time

# SQL 에서 "LOAD DATA LOCAL INFILE" 명령어를 사용하려면 "local_infile = 1" 옵션을 추가 해줘야 함
connect = pymysql.connect(host='localhost', user='root', password='han1280', db='takealook', charset='utf8', local_infile = 1)
cursor = connect.cursor(pymysql.cursors.DictCursor)

# Dataset에 절대주소로 참조할때 폴더별 구분자는 '/' 이다.
DataSet = [
    '''
            LOAD DATA LOCAL INFILE     'C:/Users/JJunJang/OneDrive/project/TakeALook_pj/pythonDB/ratings.tsv'
            INTO TABLE                 ratings
            COLUMNS TERMINATED BY      '\t'
            LINES TERMINATED BY        '\n';
    ''',
    '''
            LOAD DATA LOCAL INFILE     'C:/Users/JJunJang/OneDrive/project/TakeALook_pj/pythonDB/akas.tsv'
            INTO TABLE                 title_akas
            COLUMNS TERMINATED BY      '\t'
            LINES TERMINATED BY        '\n';
    ''',
    '''
            LOAD DATA LOCAL INFILE     'C:/Users/JJunJang/OneDrive/project/TakeALook_pj/pythonDB/basics.tsv'
            INTO TABLE                 basic_titles
            COLUMNS TERMINATED BY      '\t'
            LINES TERMINATED BY        '\n';
    ''',
    '''
            LOAD DATA LOCAL INFILE     'C:/Users/JJunJang/OneDrive/project/TakeALook_pj/pythonDB/crew.tsv'
            INTO TABLE                 crew
            COLUMNS TERMINATED BY      '\t'
            LINES TERMINATED BY        '\n';
    ''',
    '''
            LOAD DATA LOCAL INFILE     'C:/Users/JJunJang/OneDrive/project/TakeALook_pj/pythonDB/principals.tsv'
            INTO TABLE                 principals
            COLUMNS TERMINATED BY      '\t'
            LINES TERMINATED BY        '\n';
    '''
]
# 0 = ratings, 1 = title_akas, 2 = basic_titles, 3 = crew, 4 = principals

# 실행 중간에 Warning (12**, "Row or Data" ) 과 같은 오류가 여러줄 나는대 실제 서버 확인결과 누락된 값 X
# print("DataSet 서버연동중")

for i in range(0, 5):
    sql = DataSet[i]
    cursor.execute(sql)
    time.sleep(1)
    connect.commit()
    print(sql)
    time.sleep(5)

print("DataSet + Table 연동완료")

# 2019-06-07 기준 DATA
c_ratings =     ["select count(*) from ratings;"]
c_title_akas =  ["select count(*) from title_akas;"]
c_basic_titles = ["select count(*) from basic_titles;"]
c_crew =        ["select count(*) from crew;"]
c_principals =  ["select count(*) from principals;"]

tableCount = [c_ratings, c_title_akas, c_basic_titles, c_crew, c_principals]
tableC = ["930,140",
          "3,790,910",
          "5,910,765",
          "5,913,258",
          "34,029,830"]

# 2019-06-07 기준 DATA
for j in range(0, 5):
     sql = tableCount[j]
     print("명령어 : " + str(sql) + "    " + tableC[j] + "과 같아야 함")
     for s in sql:
         cursor.execute(s)
         result = cursor.fetchall()
         for r in result:
             print(r)

SQL_S1 = ["USE test;",
          '''
              delete from basic_titles
              where titleType != 'movie';
          ''']
SQL_S2 = ["USE test;",
          '''
            delete from basic_titles 
            where startYear not between 1980 and 2020 and primaryTitle <> 'Citizen Kane'
            and primaryTitle <> '12 Angry Men' 
            and primaryTitle <> 'The Godfather' 
            and primaryTitle <> 'The Godfather: Part II'
            and primaryTitle <> 'The Godfather: Part III'
            and primaryTitle <> 'Gone With The Wind'
          ''']
SQL_S3 = ['''
             delete from basic_titles 
             where startYear is null;
         ''']
SQL_S4 = ['''
            delete from ratings
            where numVotes < 5000;
         ''']
SQL_S5 = ['''
            delete from basic_titles
            where tconst not in (select tconst from ratings);
         ''']
SQL_S6 = ['''
            delete from ratings
            where tconst not in (select tconst from basic_titles);
         ''']
SQL_S7 = ['''
            SELECT * FROM basic_titles
            INTO OUTFILE 'C:/Users/JJunJang/OneDrive/project/TakeALook_pj/pythonDB/my_table.csv'
            CHARACTER SET utf8
            FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
            LINES TERMINATED BY '\n'
         ''']

SQL_Sentence = [SQL_S1, SQL_S2, SQL_S3, SQL_S4, SQL_S5, SQL_S6, SQL_S7]

print("# SQL 간소화 작업 시작")

print("# 30분소요")
for n in range(0, 7):
    sql = SQL_Sentence[n]
    print(sql)
    for s in sql:
        cursor.execute(s)
        result = cursor.fetchall()
        connect.commit()
        for r in result:
            print(r)

print("# SQL 간소화 작업 완료")

connect.close()