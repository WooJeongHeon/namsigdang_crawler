FROM python:3.9

LABEL maintainer="contact@wookingwoo.com"

RUN apt-get -y update

RUN mkdir /home/ubuntu
RUN mkdir /home/ubuntu/namsigdang-server/ # Docker에 해당 폴더 생성

# 컨테이너 내 프로젝트 root directory 설정
WORKDIR /home/ubuntu/namsigdang-server

# 해당 디렉토리를 WORKDIR에 복사
COPY ./namsigdang_crawler ./namsigdang_crawler
COPY ./requirements.txt .

RUN pip install --upgrade pip # pip 업그레이드
RUN pip install -r requirements.txt # 패키지 설치
RUN apt-get install chromium -y # 크로니움 설치

# 컨테이너 내 프로젝트 root directory 설정
WORKDIR /home/ubuntu/namsigdang-server/namsigdang_crawler

# 실행
CMD ["python", "main.py"]

# docker build --tag namsigdang-crawler:1.0 .