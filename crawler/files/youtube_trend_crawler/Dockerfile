FROM ubuntu:16.04

ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8


# 기본 패키지들 설치 및 Python 3.6 설치
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc
RUN apt-get install -y git

RUN python3.6 -m pip install pip --upgrade

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

RUN apt-get install -y tzdata

ADD . /app
WORKDIR /app

COPY requirements_yt.txt ./requirements_yt.txt
RUN pip3 install -r requirements_yt.txt

COPY yt_trend_crawler.py ./yt_trend_crawler.py

RUN touch /tmp/yt_trend_crawler.log

CMD python3.6 ./yt_trend_crawler.py >> /tmp/yt_trend_crawler.log 2>&1