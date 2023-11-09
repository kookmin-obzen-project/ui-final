
import pymysql

# 데이터베이스 연결 정보
host = 'localhost'
port = 3306
database = 'obzen_test'
username = 'root'
password = 'password'

# 데이터베이스 연결
conn = pymysql.connect(host=host, port=port, database=database, user=username, password=password)

# 커서 생성
cursor = conn.cursor()


# CHANNEL 테이블에서 STORE_NO와 STORE_NM을 가져와서 channel_data 리스트 생성
cursor.execute("SELECT STORE_NO, STORE_NM FROM CHANNEL")
rows = cursor.fetchall()
channel_data = [(store_no, store_nm) for store_no, store_nm in rows]

# 데이터베이스 연결 종료
conn.close()

# channel_data 리스트 출력 (예제로 출력함)
for data in channel_data:
    print(data)