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



# 오늘 날짜 함수
def get_today():
    now = time.localtime()
    today = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    today_ = today + "/"
    return today_

# 날짜 함수 -> 변수 대입
today_dir = get_today()


# SQL
SQL_Use = "USE takealook;"

SQL_S1 = """
            ALTER TABLE basic_titles
	        ADD COLUMN titleKor VARCHAR(415) NULL DEFAULT NULL AFTER primaryTitle;
        """

SQL_S2 = """
            DELETE FROM basic_titles
            WHERE titleType != 'movie';
        """

SQL_S3 = """
            DELETE FROM basic_titles 
            WHERE startYear not between 1980 and 2020 and primaryTitle <> 'Citizen Kane'
            and primaryTitle <> '12 Angry Men' 
            and primaryTitle <> 'The Godfather'     
            and primaryTitle <> 'The Godfather: Part II'
            and primaryTitle <> 'The Godfather: Part III'
            and primaryTitle <> 'Gone With The Wind';
        """

SQL_S4 = """
             DELETE FROM basic_titles 
             WHERE startYear is null;
        """

SQL_S5 = """
            DELETE FROM ratings
            WHERE numVotes < 5000;
        """

SQL_S6 = """
            DELETE FROM ratings
            WHERE averagerating <= 4.0;
        """

SQL_S7 = """
            DELETE FROM basic_titles
            WHERE tconst not in (SELECT tconst FROM ratings);
        """

SQL_S8 = """
            DELETE FROM ratings
            WHERE tconst not in (SELECT tconst FROM basic_titles);
        """

SQL_S9 = """
            DELETE FROM basic_names
            WHERE nconst NOT IN (SELECT nconst FROM principals);
        """


SQL_Sentence = [SQL_S1, SQL_S2, SQL_S3, SQL_S4, SQL_S5, SQL_S6, SQL_S7, SQL_S8]
optimizeList = ["basic_titles", "basic_titles", "basic_titles", "basic_titles", "ratings",
                "ratings", "basic_titles", "ratings"]

for i in range(len(SQL_Sentence)):
    sql_time_start = time.time()
    sql = SQL_Sentence[i]
    # sql_op = """
    #         optimize table """ + optimizeList[i] + """;
    #     """
    print("\n[" + str(i+1) + "번 sql Load]" + sql)
    cursor.execute(SQL_Use)
    # cursor.execute(sql_op)
    result = cursor.fetchall()
    connect.commit()
    print("[ " + str(i+1) + "번 sql ]ㅡㅡㅡ #Commit ㅡㅡㅡ")
    sql_time = time.time()
    print(time.strftime("[%y-%m-%d] %X", time.localtime()))  # 현재시간 출력
    print(" 소요시간 : %s초\n" \
          % (round(sql_time - sql_time_start, 1)))


# processing end
total_end = time.time()
total_end_time = time.strftime("[%y%m%d] %X", time.localtime())

# print processing time
print("%s ~ %s, 소요시간 : %s초" \
    %(total_start_time, total_end_time, round(total_end - total_start, 1)))

# SQL SERVER disconnect
connect.close()
