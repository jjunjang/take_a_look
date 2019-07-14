import pymysql

connect = pymysql.connect(host='127.0.0.1', user='root', password='han1280', db='takealook', charset='utf8', local_infile = 1)
# AWS RDS : takealook.cjdwnzzk2agh.ap-northeast-2.rds.amazonaws.com
cursor = connect.cursor(pymysql.cursors.DictCursor)

# 'execute' 메소드에 for문을 이용하여 실행할 쿼리문을 전달하고 'fetchall' 메소드를 이용하여 쿼리문을 실행하였습니다.
# DB 생성 후 조회 쿼리를 마지막에 담아 출력해보니 test DB가 제대로 생성되어있었습니다.

# 각 테이블 sql 명령어

reset = [
        "DROP DATABASE IF EXISTS takealook;",
        "CREATE DATABASE takealook;"
        ]

crew = ["USE takealook;",
        '''
            CREATE TABLE crew (
                tconst VARCHAR(20) NOT NULL,
                directors TEXT NULL DEFAULT NULL,
                writers TEXT NULL DEFAULT NULL
            )
            engine = innoDB default
            charset = utf8;
        ''']

ratings = ["USE takealook;",
           '''
                CREATE TABLE ratings (
                    tconst VARCHAR(20) NOT NULL,
                    averageRating FLOAT NULL DEFAULT NULL,
                    numVotes INT(10) NULL DEFAULT NULL
                )
                engine = innoDB default
                charset = utf8;
           ''']

principals = ["USE takealook;",
              '''
                    CREATE TABLE principals (
                        tconst VARCHAR(20) NOT NULL,
                        ordering INT(11) NULL DEFAULT NULL,
                        nconst VARCHAR(20) NULL DEFAULT NULL,
                        category TEXT NULL DEFAULT NULL,
                        job TEXT NULL DEFAULT NULL,
                        characters TEXT NULL DEFAULT NULL
                    )
                    engine = innoDB default
                    charset = utf8;
              ''']

title_akas = ["USE takealook;",
              '''
                  CREATE TABLE title_akas (
                      titleId VARCHAR(20) NOT NULL,
                      ordering INT(10) NULL DEFAULT NULL,
                      title VARCHAR(2048) NULL DEFAULT NULL,
                      region VARCHAR(10) NULL DEFAULT NULL,
                      language VARCHAR(10) NULL DEFAULT NULL,
                      types VARCHAR(20) NULL DEFAULT NULL,
                      attributes VARCHAR(256) NULL DEFAULT NULL,
                      isOriginalTitle VARCHAR(2048) NULL DEFAULT NULL
                  )
                  engine = innoDB default
                  charset = utf8;
              ''']

basic_titles = ["USE takealook;",
               '''
                    CREATE TABLE basic_titles (
                        tconst VARCHAR(20) NOT NULL,
                        titleType VARCHAR(20) NULL DEFAULT NULL,
                        primaryTitle VARCHAR(128) NULL DEFAULT NULL,
                        originalTitle VARCHAR(128) NULL DEFAULT NULL,
                        isAdult VARCHAR(50) NULL DEFAULT NULL,
                        startYear VARCHAR(50) NULL DEFAULT NULL,
                        endYear VARCHAR(50) NULL DEFAULT NULL,
                        runtimeMinutes VARCHAR(50) NULL DEFAULT NULL,
                        genres VARCHAR(128) NULL DEFAULT NULL
                    )
                    engine = innoDB default
                    charset = utf8;
               ''']

SQL_table = [reset, crew, ratings, principals, title_akas, basic_titles]

print("초기화 및 Table 생성중")

for i in range(0, 6):
    sql = SQL_table[i]
    print(str(i+1) + " 번 테이블 생성완료")
    for s in sql:
        cursor.execute(s)
        result = cursor.fetchall()
        for r in result:
            print(r)

connect.close()
print("끗")