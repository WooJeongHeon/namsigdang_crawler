# namsigdang(남식당)

## chrome 설치

크롬 버전보기 리눅스 명령어:

```bash
$ google-chrome --version
```

현재 크롬 사용 버전:

```
Google Chrome 73.0.3683.103
```

크롬 설치

```bash
$ cd namsigdang/namsigdang_crawler/setup_files
$ sudo dpkg -i google-chrome-stable_current_amd64.deb
$ sudo apt-get install -f

```

참고 사이트

```
https://christopher.su/2015/selenium-chromedriver-ubuntu/
```

## 사용법 (Getting Started)

### namsigdang Django server

가상환경 실행

```bash
$ source venv/bin/activate
```

DB 생성

```bash
$ python3 manage.py makemigrations

```

DB migrate

```bash
$ python3 manage.py migrate

```

BackEnd 서버 실행

```bash
$ python3 manage.py runserver
```

Django에서 기본 python manage.py runserver 로 실행시 기본 포트번호가 8000으로 지정되어 있습니다. 아래와 같은 방법으로 포트 번호를 변경하거나 외부접속을 허용할 수 있습니다.

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

#### file information

main.py : 메인 크롤러

classify_data_in_date.py : namsigdang/namsigdang_crawler/data/crawling_menu/all_menu.dat으로부터 년, 월로 분류하여
namsigdang/namsigdang_crawler/data/crawling_menu에 year_2020/month_08/2020_08_menu.dat와 같이 저장. (Django App API에서 해당 Data
사용)

