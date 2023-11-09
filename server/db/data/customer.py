
from faker import Faker
import random

# Faker 객체 생성
fake = Faker()

import pymysql

# 데이터베이스 연결 정보
host = 'localhost'
port = 3306
database = 'obzen'
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
# for data in channel_data:
#     print(data)


# 30개의 가짜 데이터 생성
for _ in range(30):
    cust_no = fake.unique.random_int(min=199220000000, max=202329999999)  # 고객 번호 (무작위 범위 설정)
    age = random.choice(['10대 이하', '20대', '30대', '40대', '50대', '60대', '70대', '80대 이상'])  # 나이
    frgn_cd_nm = random.choice(['내국인', '외국인'])  # 내외국인
    mng_store_cd, mng_store_cd_nm = random.choice(channel_data)  # 채널 테이블에서 무작위 선택
    channel_second = random.choice(['가맹점', '농협', '대형마트', '백화점', '면세점', '직영점'])  # 채널
    gndr_cd_nm = random.choice(['여성', '남성'])  # 성별
    birth_year = fake.random_int(min=1970, max=2020)
    birth_month = fake.random_int(min=1, max=12)
    birth_day = fake.random_int(min=1, max=31)
    birth_date = int(f"{birth_year}{birth_month}{birth_day}")
    tm_yn = random.choice(['Y', 'N'])  # 플래그
    sms_yn = random.choice(['Y', 'N'])  # 플래그
    join_date = fake.date_this_decade().strftime('%Y%m%d')  # 가입일자
    withdraw_cd_nm = random.choice(['탈퇴', '정상'])  # 탈퇴 여부
    cust_seg_cd_nm = random.choice(['일반', '법인', '사내'])  # 고객 세그먼트
    cust_grd_cd_nm = random.choice(['ROYAL GOLD', 'SILVER', 'GOLD', 'FAMILY'])  # 고객 등급
    prmtd_date = fake.date_this_decade().strftime('%Y%m%d')  # 프로모션 일자
    cust_grd_cd_nm_last = random.choice(['GOLD', 'SILVER', 'FAMILY'])  # 최근 고객 등급
    subsc_path_cd_nm = random.choice(['공식쇼핑몰', '매장', '네이버페이', '삼성페이', '케어나우', 'KAKAO'])  # 가입 경로
    point_bal = fake.random_int(min=0, max=5000)  # 포인트 잔액 (무작위 범위 설정)
    point_exp = fake.random_int(min=0, max=1000)  # 포인트 만료 (무작위 범위 설정)
    point_bfh = fake.random_int(min=0, max=500)  # 포인트 사용 (무작위 범위 설정)

    # 생성된 가짜 데이터 출력 또는 데이터베이스에 삽입할 수 있습니다.
    print(f"('{cust_no}', '{age}', '{frgn_cd_nm}', {mng_store_cd}, '{mng_store_cd_nm}', '{channel_second}', '{gndr_cd_nm}', '{birth_year}', '{birth_date}', '{tm_yn}', '{sms_yn}', '{join_date}', '{withdraw_cd_nm}', '{cust_seg_cd_nm}', '{cust_grd_cd_nm}', '{prmtd_date}', '{cust_grd_cd_nm_last}', '{subsc_path_cd_nm}', {point_bal}, {point_exp}, {point_bfh}),")