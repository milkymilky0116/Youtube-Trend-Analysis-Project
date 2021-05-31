
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
DEVELOPER_KEY="AIzaSyAse67X9AAIXmK1UAPAcI8Ju71y9pijHnc"
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION="v3"

def youtube_comment_search(video_id):
    youtube=build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    comment_responce=youtube.commentThreads().list(
        part="snippet,replies",
        videoId=video_id
    ).execute()

    comment_section={}
    reply=[]

    while comment_responce:
        for comment_result in comment_responce["items"]:
            comment=comment_result['snippet']["topLevelComment"]['snippet']['textDisplay']
            replycount=comment_result['snippet']['totalReplyCount']
            if replycount>0:
                for replycomments in comment_result['replies']['comments']:
                    reply.append(replycomments['snippet']['textDisplay'])
            comment_section[comment]=reply
            reply=[]

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