# namsigdang(남식당)

## 설치

apt-get install python3-pip

```bash
$ pip install Selenium
```

pip3 install beautifulsoup4


## 사용법 (Getting Started)


### namsigdang Django server

가상환경 실행
```bash
$ source venv/bin/activate
```

BackEnd 서버 실행
```bash
$ python3 manage.py runserver
```

Django에서 기본 python manage.py runserver 로 실행시 기본 포트번호가 8000으로 지정되어 있습니다.
아래와 같은 방법으로 포트 번호를 변경하거나 외부접속을 허용할 수 있습니다.



포트번호 변경 (예시: 8080)
```bash
$ python3 manage.py runserver 8080
```
외부접속 허용
```bash
$ python3 manage.py runserver 0.0.0.0:8080
```
```bash
$ python3 manage.py runserver 0:8080
```

---

### namsigdang crawler

```bash
$ nohup python3 main.py &
```
