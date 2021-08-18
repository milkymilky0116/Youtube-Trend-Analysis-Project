# Youtube-Trend-Analysis-Project 
#(유튜브 실시간 트렌드 검색 프로젝트)

### :video_camera: Tensorflow, Word2Vec, Multi-criteria Decision 등을 이용한 실시간 유튜브 트렌드 프로젝트   


### :pencil2:개발동기

```
최근 네이버를 비롯한 검색엔진 사이트에서 점차 실시간 검색어 서비스가 사라지고 있는 추세입니다. 
물론 실시간 검색어 서비스가 여러가지 문제점들로 인해 역사의 뒷편으로 사라진것은 사실이지만,
다소 나이가 있으신 연령대 분들, 혹은 트렌드를 바로바로 체크해야 하는 인플루언서 분들이
최근 나타나고 있는 사회적인 이슈들을 즉각적으로 확인하기가 어렵다는사실을 알게 되었습니다. 

그래서 저희는 Tensorflow, Word2vec, 자연어 처리 기법등을 이용하여 데이터를 분석하여
누구나 쉽게 볼 수 있는 실시간 트렌드 서비스를 개발하고자 합니다.
데이터 수집은 최근 많은 연령층을 아우르고 있는 플랫폼인 유튜브를 통해 진행하기로 하였습니다.
```
***
### 기능
```
1.실시간 키워드 수집기
-Word2vec을 이용한 연관단어 검색
-댓글 수집 및 감정분석
-키워드 요약
-sns(트위터)에서의 선호도 파악

2.웹 플랫폼
-동영상에 대한 조회수 변화, 긍/부정/중립 통계, 상위 댓글 10개 및 여론 확인
-현재 인기 동영상들의 키워드 확인 및 검색기능

```

### 플라스크 웹서버 설치 (로컬)

```
git clone https://github.com/MangoSteen0903/Youtube-Trend-Analysis-Project.git
```

원하는 위치에 git을 클론합니다.

```
pip install -r requirements.txt
```

모듈들을 위해 requirements 안에 있는 모듈들을 설치합니다.

```
python app.py
```
app.py를 실행합니다.

### 플라스크 웹서버 설치 (아코디언 (CI/CD)- Flask 설정)

![image](https://user-images.githubusercontent.com/84823612/129846460-ad752df9-ffa9-4164-b68f-3994a5cd6c42.png)

아코디언의 템플릿 탭으로 이동합니다.

![image](https://user-images.githubusercontent.com/84823612/129847113-b2c66fd8-b77a-41ab-9c43-ef0bd2c8cd88.png)

Dockerfile 탭으로 이동하여 flask 도커파일을 생성합니다.

```
FROM ubuntu:18.04

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash
RUN apt-get update -y
RUN apt-get install -y build-essential
RUN apt-get install -y python python3 python3-dev python3-pip
RUN apt-get install -y libpq-dev
RUN pip3 install --upgrade pip

ENV LANG C.UTF-8


RUN apt-get install -y wget


RUN apt-get install -y libcurl4-openssl-dev libssl-dev
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN apt-get update -y
RUN apt-get install -y openjdk-8-jre openjdk-8-jdk

COPY ./requirements.txt /app/server/
WORKDIR /app/server

RUN pip3 install -r requirements.txt

COPY . /app

WORKDIR /app

ENV POSTGRES_PASSWORD password

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["app.py"]
```

![image](https://user-images.githubusercontent.com/84823612/129847150-e0a1ab64-de77-400f-a195-2dead6025a01.png)
템플릿 탭으로 이동하여 flask를 생성합니다.

템플릿 설정탭에서, 앞서 만들어두었던 Dockerfile을 할당합니다.

![image](https://user-images.githubusercontent.com/84823612/129847282-6eda61dd-3e81-47f7-9e5e-a5245bdaf728.png)

YAML 파일에서, Container port를 5000으로 설정합니다.

![image](https://user-images.githubusercontent.com/84823612/129847340-380285a0-72fa-4059-8f18-81418a4f6845.png)

### 플라스크 웹서버 설치 (아코디언 (CI/CD)- Flask 앱생성)

앞선 Flask 설정을 완료하셨다면, 앱-> 앱추가를 눌러보시면 flask가 설정되어 있을것입니다. (로고는 별도로 설정해두셔야 합니다.)

![image](https://user-images.githubusercontent.com/84823612/129847559-94c52e51-63d0-4cc0-ad48-9a4d10128789.png)

앱생성에서 앱의 이름을 적고, Repository URL을 해당 레파지토리 주소로 입력합니다. 그리고 Git reference를 main으로 설정합니다. 
(기본은 master로 설정되어 있기 때문에 reference를 설정해두지 않을경우 에러가 생기게 됩니다.)

![image](https://user-images.githubusercontent.com/84823612/129847640-0da3f64a-392e-4492-b420-bf64aa2a93f3.png)

추가옵션에서 Service type을 Node port로 설정합니다. (Load Balancer를 설정해두었을 경우 해당 서버의 Load Balancer를 사용하셔도 무방합니다)

![image](https://user-images.githubusercontent.com/84823612/129847908-9a249fc6-0543-488e-ba53-3ad03c453692.png)

앱 생성을 누르시면 밑에 사진처럼 정상적으로 앱이 생성됩니다.

![image](https://user-images.githubusercontent.com/84823612/129847981-d3093749-4bf8-4c48-a2f2-57604f74d7f9.png)

빌드 로그를 확인해보시면 정상적으로 빌드가 되고 있는것을 확인하실 수 있습니다.

![image](https://user-images.githubusercontent.com/84823612/129848262-98d8310e-c026-4da0-95d1-5281d097bc91.png)

정상적으로 앱이 Deploy 되었는지 확인해보시려면, 앱을 클릭해서 POD를 클릭합니다.

![image](https://user-images.githubusercontent.com/84823612/129848382-44be36a2-b28a-4612-a377-ae22fc5ed9e4.png)

해당 로그가 아래와 같이 나타나게 된다면 설치에 성공한것입니다.

![image](https://user-images.githubusercontent.com/84823612/129848464-71d23428-dab4-4058-bea3-9f5f90d36f77.png)

이제 앱에서 해당 항목을 클릭하면 정상적으로 웹페이지가 열리는것을 확인 할 수 있습니다.

![image](https://user-images.githubusercontent.com/84823612/129848538-418413af-77e0-4d54-ace4-3766b5ec543a.png)


### 크롤러 설치 가이드

크롤러를 정상적으로 실행 시키기 위해서는 16GB 이상의 램을 갖춘 서버에서 실행하는 것을 권장 드립니다. (Tensorflow 모델이 내장되어 있기 때문에 이 과정에서 램 소모량이 많이 늘어나는 것으로 추측됩니다.)

크롤러 파일들은 해당 레파지토리의 crawler 폴더안에 있습니다. View count와 Youtube_trend_crawler 두개의 도커 이미지를 생성하셔야 웹서버의 모든 기능들을 확인 하실수 있습니다.

```
View count: DB에 존재하는 동영상들의 조회수를 시간단위로 수집하여 youtube_view_data DB에 저장합니다.

Youtube_trend_crawler: 저희 프로젝트의 메인 파일로, 키워드를 수집하여 유튜브 동영상의 데이터를 수집하고 분석하여 DB에 저장하는 역할을 하게 됩니다.
```

해당 폴더의 경로로 이동하여, 도커 이미지를 생성합니다.

```
docker build . -t <이미지 이름>
```

도커파일들은 Cron job에 대응하도록 작성되어 있기 때문에, 반드시 서버에서 도커 이미지에 대한 Cron job을 등록시켜주셔야 파일이 실행됩니다.

Cronjob을 등록시키기 위해, 서버에서 다음과 같은 커맨드를 입력합니다.

```
crontab -e
```

커맨드를 입력하시면 다음과 같은 화면이 나타나게 됩니다.

![image](https://user-images.githubusercontent.com/84823612/129850110-b43a3037-a075-4069-ad78-daa2a631ff05.png)

해당 에디터에서 다음과 같이 입력합니다.

```
* * * * * docker run -v /tmp:/tmp <이미지 이름>
```

별표는 cron 문법입니다. 자세한 사항은 https://en.wikipedia.org/wiki/Cron를 참조해주세요. 해당 프로젝트에서는 매 시간 단위로 크롤러를 실행시키는 것을 권장드리고 있습니다.

로그는 /tmp에 저장되어 로그를 별도로 확인하실 수 있습니다.


