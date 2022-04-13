#!/bin/sh

cd /home/ubuntu/namsigdang-server/namsigdang_crawler
sudo /usr/bin/python3 main.py

# 0 */6 * * * /home/ubuntu/namsigdang-server/namsigdang_crawler/start_namsigdang_crawling.sh > /home/ubuntu/namsigdang-server/namsigdang_crawler/data/log/crontab_log/`date +\%Y\%m\%d`_`date +\%H\%M\%S`.log 2>&1
