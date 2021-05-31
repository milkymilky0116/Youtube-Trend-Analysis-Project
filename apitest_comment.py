#Youtube API를 불러오기 위해 Google-api-client 모듈을 불러옴
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

#API KEY는 구글 클라우드 서비스에서 제공 받았고 앱이 제대로 실행되기 위해서는 키가 있어야함
DEVELOPER_KEY="AIzaSyAse67X9AAIXmK1UAPAcI8Ju71y9pijHnc"
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION="v3"

def youtube_comment_search(video_id):
    youtube=build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    #댓글을 불러오기 위해 동영상에 있는 commentThread들을 검색함
    comment_responce=youtube.commentThreads().list(
        part="snippet,replies",
        videoId=video_id
    ).execute()

    comment_section={}
    reply=[]
    #태그에 있는 특정한 정보들 (댓글과 밑에 있는 답글의 내용)을 추출함
    while comment_responce:
        for comment_result in comment_responce["items"]:
            comment=comment_result['snippet']["topLevelComment"]['snippet']['textDisplay']
            replycount=comment_result['snippet']['totalReplyCount']
            #따로 replycount 조건을 건 이유는 답글이 없는 댓글도 있기 때문에 구분하여 추출하기 위함
            if replycount>0:
                for replycomments in comment_result['replies']['comments']:
                    reply.append(replycomments['snippet']['textDisplay'])
            comment_section[comment]=reply #댓글과 답글의 정보를 dict형태로 저장함
            reply=[]

        #comment_responce는 몇개의 댓글들만 뽑아올 수 있는데, nextPageToken이 있으면 표시할 댓글이 남아있다는 뜻이므로
        #nextPageToken이 없어질때까지 모든 댓글 정보를 긁어옴
        if 'nextPageToken' in comment_responce:
            page_Token=comment_responce['nextPageToken']
            comment_responce = youtube.commentThreads().list(
                    part = 'snippet,replies',
                    pageToken=page_Token,
                    videoId = video_id
                ).execute()
        else:
            break
    return comment_section
video_id="ww6uRd4s-Ik"
result=youtube_comment_search(video_id)
for item in result:
    print("Comment: %s\treplies: %s" % (item,result[item]))