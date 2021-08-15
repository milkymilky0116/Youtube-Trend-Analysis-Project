#!/bin/bash

# 크론탭으로 실행되는 프로그램은 환경변수가 없으므로 설정해준다.
export PATH=$PATH:.:/bin
export JAVA_HOME=/usr/java/
export PATH=$PATH:/home/usr/java/

# 해당 프로그램 위치로 이동, 이동하지 않으면 기본적으로 설정된 유저의 홈에서 실행
python3 /mnt/a/server/docker/youtube_trend_crawler/yt_trend_crawler.py