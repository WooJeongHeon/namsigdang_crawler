# namsigdang crawler

## Get started with Docker

```bash
docker build --tag namsigdang-crawler:1.0 .
```

## File Information

- main.py : 메인 크롤러

- classify_data_in_date.py : namsigdang/namsigdang_crawler/data/crawling_menu/all_menu.dat으로부터 년, 월로 분류하여
  namsigdang/namsigdang_crawler/data/crawling_menu에 year_2020/month_08/2020_08_menu.dat와 같이 저장. (Django App API에서 해당
  Data 사용)

## Installing Chrome Specific Versions

- How to check your Chrome version

```bash
$ google-chrome --version
```

- Installing Chrome

```bash
$ cd namsigdang/namsigdang_crawler/setup_files
$ sudo dpkg -i google-chrome-stable_current_amd64.deb
$ sudo apt-get install -f

```

- 참고 사이트

```
https://christopher.su/2015/selenium-chromedriver-ubuntu/
```
