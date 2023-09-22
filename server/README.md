# python version: python3 --version == Python 3.10.6

# pip version: pip --version: pip 23.2.1

# fastapi install: pip install "fastapi[all]"

# server start: uvicorn [file]:app --host=[host] --port=[port] --reload // default port: 8000

# Swagger UI: 127.0.0.1:[port]/docs

# DB start for mac

## brew services start mariadb //실행

## brew services stop mariadb //중단

## brew services list //실행중인지 상태 확인

# server 접속
1. 루트 경로  uvicorn main:app --host=127.0.0.1 --port=8080 --reload 
2. DB 접속 및 core - base.py 에서 URL 변경 

# DB 연결 
1. db - .env.db 에서 본인 db_url 입력 
ex. db_url='mysql+pymysql://[user_name]:[user_password]@[user_localhost]/[DB_name]'

# api 명세서
1. 서버를 실행합니다. 
2. http://[host]:[port]/docs 에 접속합니다. 
ex. "uvicorn main:app --host=127.0.0.1 --port=8080 --reload" 로 서버를 실행할 경우
    http://127.0.0.1:8080/docs 에 접속합니다.