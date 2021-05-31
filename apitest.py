from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
DEVELOPER_KEY="AIzaSyAse67X9AAIXmK1UAPAcI8Ju71y9pijHnc"
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION="v3"

def youtube_search():
    youtube=build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

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