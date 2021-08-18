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

### UI

![image](https://user-images.githubusercontent.com/84823612/129853607-dea2ba67-2102-442b-9a32-067998f59b8b.png)


### 플라스크 설치 가이드

자세한 사항은 해당 프로젝트의 위키에서 Flask 설치 가이드 를 참조해주세요. [Flask 설치 가이드](https://github.com/MangoSteen0903/Youtube-Trend-Analysis-Project/wiki/Flask-%EC%84%A4%EC%B9%98-%EA%B0%80%EC%9D%B4%EB%93%9C)

### 크롤러 설치 가이드

자세한 사항은 해당 프로젝트의 위키에서 Crawler 설치 가이드를 참조해주세요. [Crawler 설치 가이드](https://github.com/MangoSteen0903/Youtube-Trend-Analysis-Project/wiki/Crawler-%EC%84%A4%EC%B9%98-%EA%B0%80%EC%9D%B4%EB%93%9C)

***
### Collecting Data / Analysis

![image](https://user-images.githubusercontent.com/84823612/129851961-9cfc4230-c069-4d92-bcfd-b08d5594db0b.png)

크롤러의 프로세스는 총 6가지 과정을 거쳐서 진행이 됩니다.

```
1. 데이터 수집 (Selenium)
2. 동영상 파싱 (조회수, 제목, 좋아요 수... 같은 메타데이터를 얻어옴) (pytube 모듈)
3. 키워드 요약 (Sentence-Transformers)
4. 댓글 감정분석 (Youtube Data API, CLOVA Sentiment API)
5. 데이터 랭킹 (Multi-Criteria Decision, Twitter API)
6. DB 저장
```

### Word2vec 모델 테스트

해당 프로젝트에서 주요하게 쓰인 Word2vec 모델에 대해서 모델을 시각화하는 기능을 제공하고 있습니다. visualization에 해당 파일들이 저장되어 있습니다.

실행시키기 위해서는 Gensim의 Word2vec, pyvis 모듈 설치가 필요합니다.

vis_word_map.py에서 make_word_map에 원하는 키워드를 넣으시고 실행시키면 Node와 edge로 구성된 단어 관계도가 표시됩니다.

![image](https://user-images.githubusercontent.com/84823612/129853424-1cc7e6ab-50c1-4bc3-bf1e-7f56568a8690.png)

![image](https://user-images.githubusercontent.com/84823612/129853460-e2688fa1-519b-41e5-ad09-a0b50f241484.png)

자신만의 Word2vec 모델을 시각화 하고 싶으신경우, 해당 위키를 참고해주시기 바랍니다. [Word2vec 사용기]()
