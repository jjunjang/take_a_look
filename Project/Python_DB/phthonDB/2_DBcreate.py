# -*- coding: utf-8 -*-
import pymysql
import time

# 스크립트 시작
total_start = time.time()
total_start_time = time.strftime("[%y%m%d] %X", time.localtime())


# Local DB
connect = pymysql.connect(host='localhost',
                          user='root', password='han1280', db='takealook', charset='utf8', local_infile=1)
# RDS SERVER DB
# connect = pymysql.connect(host='takealook.cjdwnzzk2agh.ap-northeast-2.rds.amazonaws.com',
#                           user='tal_admin', password='take1234', db='takealook', charset='utf8', local_infile=1)

cursor = connect.cursor(pymysql.cursors.DictCursor)

# 'execute' 메소드에 for문을 이용하여 실행할 쿼리문을 전달하고 'fetchall' 메소드를 이용하여 쿼리문을 실행하였습니다.
# DB 생성 후 조회 쿼리를 마지막에 담아 출력해보니 test DB가 제대로 생성되어있었습니다.

# 각 테이블 sql 명령어

reset = [
        "DROP DATABASE IF EXISTS takealook;",
        "CREATE DATABASE takealook;"
        ]

basic_titles = ["USE takealook;",
               """
                    CREATE TABLE basic_titles (
                        tconst VARCHAR(10) NOT NULL,
                        titleType VARCHAR(20) NULL,
                        originalTitle VARCHAR(415) NULL,
                        titleKor VARCHAR(415) NULL,
                        isAdult VARCHAR(2) NULL,
                        startYear VARCHAR(10) NULL,
                        endYear VARCHAR(10) NULL,
                        runtimeMinutes VARCHAR(10) NULL,
                        genres VARCHAR(50) NULL,
                        PRIMARY KEY (tconst)
                    )
                    engine = innoDB default
                    charset = utf8;
               """]
# ↑ originalTitle VARCHAR(415) NULL,
#    isAdult VARCHAR(50) NULL DEFAULT NULL, [DROP 必]
#    endYear VARCHAR(50) NULL DEFAULT NULL,
#    runtimeMinutes VARCHAR(50) NULL DEFAULT NULL,


crew = ["USE takealook;",
        """
            CREATE TABLE crew (
                tconst VARCHAR(10) NOT NULL,
                directors TEXT NULL,
                writers TEXT NULL,
                PRIMARY KEY (tconst),
                CONSTRAINT fk_titles_crew FOREIGN KEY (tconst) REFERENCES basic_titles(tconst) ON UPDATE CASCADE ON DELETE CASCADE
            )
            engine = innoDB default
            charset = utf8;
        """]

ratings = ["USE takealook;",
           """
                CREATE TABLE ratings (
                    tconst VARCHAR(10) NOT NULL,
                    averageRating FLOAT NULL,
                    numVotes INT(10) NULL,
                    PRIMARY KEY (tconst),
                    CONSTRAINT fk_titles_ratings FOREIGN KEY (tconst) REFERENCES basic_titles(tconst) ON UPDATE CASCADE ON DELETE CASCADE
                )
                engine = innoDB default
                charset = utf8;
           """]

principals = ["USE takealook;",
              """
                    CREATE TABLE principals (
                        tconst VARCHAR(10) NOT NULL,
                        ordering TINYINT(1) NOT NULL,
                        nconst VARCHAR(10) NOT NULL,
                        category VARCHAR(30) NULL,
                        job VARCHAR(900) NULL,
                        characters VARCHAR(900) NULL,
                        PRIMARY KEY (tconst, ordering),
                        CONSTRAINT fk_titles_principals FOREIGN KEY (tconst) REFERENCES basic_titles(tconst) ON UPDATE CASCADE ON DELETE CASCADE
                    )
                    engine = innoDB default
                    charset = utf8;
              """]

basic_names = ["USE takealook;",
               """
                    CREATE TABLE basic_names (
                        nconst VARCHAR(10) NOT NULL,
                        primaryName VARCHAR(128) NULL,
                        birthYear VARCHAR(10) NULL,
                        deathYear VARCHAR(10) NULL,
                        primaryProfession TEXT NULL,
                        knownForTitles TEXT NULL,
                        PRIMARY KEY (nconst)
                    )
                    engine = innoDB default
                    charset = utf8;
               """]
# CONSTRAINT fk_principals_names FOREIGN KEY (nconst) REFERENCES principals(nconst) ON UPDATE CASCADE ON DELETE CASCADE
# ↑ primaryProfession TEXT NULL, [DROP 必]
#    knownForTitles TEXT NULL

emotion = ["USE takealook;",
               """
                    CREATE TABLE emotion (
                        tconst VARCHAR(10) NOT NULL,
                        emotionTags VARCHAR(80) NOT NULL,
                        emotioonName VARCHAR(80) NULL,
                        emotionScore VARCHAR(10) NULL,
                        PRIMARY KEY (tconst),
                        CONSTRAINT fk_title_emotion FOREIGN KEY (tconst) REFERENCES basic_titles(tconst) ON UPDATE CASCADE ON DELETE CASCADE
                    )
                    engine = innoDB default
                    charset = utf8;
               """]

userinfo = ["USE takealook;",
               """
                    CREATE TABLE userinfo (
                        userid VARCHAR(20) NOT NULL,
                        userpw VARCHAR(30) NULL,
                        gender TINYINT(1) NULL,
                        age TINYINT(1) NULL,
                        email VARCHAR(96) NULL,
                        PRIMARY KEY (userid)
                    )
                    engine = innoDB default
                    charset = utf8;
               """]

appraisal = ["USE takealook;",
               """
                    CREATE TABLE appraisal (
                        userid VARCHAR(20) NOT NULL,
                        tconst VARCHAR(10) NOT NULL,
                        movie_score TINYINT(1) NULL,
                        recommend TINYINT(1) NULL,
                        PRIMARY KEY (userid, tconst),
                        CONSTRAINT fk_userinfo_appraisal FOREIGN KEY (userid) REFERENCES userinfo(userid) ON UPDATE CASCADE ON DELETE CASCADE,
                        CONSTRAINT fk_titles_appraisal FOREIGN KEY (tconst) REFERENCES basic_titles(tconst) ON UPDATE CASCADE ON DELETE CASCADE
                    )
                    engine = innoDB default
                    charset = utf8;
               """]

SQL_TABLE = [reset, basic_titles, crew, ratings, principals, basic_names, emotion, userinfo, appraisal]




print("초기화 및 테이블 생성중")

for i in range(len(SQL_TABLE)):
    sql = SQL_TABLE[i]
    print("# [" + str(i+1) + "] TABLE 생성완료")
    for s in sql:
        cursor.execute(s)
        result = cursor.fetchall()
        for r in result:
            print(r)

# processing end
total_end = time.time()
total_end_time = time.strftime("[%y%m%d] %X", time.localtime())

# print processing time
print("%s ~ %s, 소요시간 : %s초" \
    %(total_start_time, total_end_time, round(total_end - total_start, 1)))

# SQL SERVER disconnect
connect.close()
print("# Finish")