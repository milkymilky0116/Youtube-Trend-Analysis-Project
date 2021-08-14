FROM ubuntu:16.04

ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8


RUN apt-get update && apt-get install -y \
    software-properties-common

# Add the "JAVA" ppa
RUN add-apt-repository -y \
    ppa:webupd8team/java

# Install OpenJDK-8
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME



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

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY yt_trend_crawler.py ./yt_trend_crawler.py

RUN touch /tmp/yt_trend_crawler.log

CMD python3.6 ./yt_trend_crawler.py >> /tmp/yt_trend_crawler.log 2>&1