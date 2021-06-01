#Youtube API를 불러오기 위해 Google-api-client 모듈을 불러옴
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#API KEY는 구글 클라우드 서비스에서 제공 받았고 앱이 제대로 실행되기 위해서는 키가 있어야함
DEVELOPER_KEY="AIzaSyAse67X9AAIXmK1UAPAcI8Ju71y9pijHnc"
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION="v3"

def youtube_search():
    #기본적인 API 객체를 설정함
    youtube=build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)


    #검색할 매개변수와 옵션을 설정하여 search_responce에 설정함
    search_responce=youtube.search().list(
        q="스테이크",
        pageToken='CDIQAA',
        order="rating",
        part="snippet",
        maxResults=50
    ).execute()

    videos=[]
    channels=[]
    playlists=[]

    
    #GET으로 받은 태그들에서 원하는 정보들(video 이름, 채널 이름, 플레이리스트 이름) 만 추출해서 리스트의 형태로 저장함
    for search_result in search_responce.get("items",[]):
        
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s) " % (search_result["snippet"]["title"],
                                 search_result["id"]["videoId"]))
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))
    return videos
    
result=youtube_search()
for i in range(len(result)):
    print(result[i])
