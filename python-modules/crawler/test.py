from googleapiclient.discovery import build
import re

def comment_crawler(api_key,video_link):
    youtube = build('youtube', 'v3',developerKey=api_key)

    #/watch?v=hEqJLnEWVKk

    video_link=video_link[video_link.find("=")+1:]

    video_id=video_link
  
    video_response=youtube.commentThreads().list(
    part='snippet',
    videoId=video_id,
    maxResults=30
    ).execute()
    result=[]

 
    while True:
        for item in video_response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            cleaner=re.compile('<.*?>')
            comment=re.sub(cleaner,'',comment)         
            result.append(comment)
        if len(video_response['items'])<30:
            if len(result)==len(video_response['items']):
                break
        if len(result)==30:
            break
    return result

print(comment_crawler('AIzaSyA8AVDeWVW2aEqMds7z51gjhr8o3ebRyik','/watch?v=hz3GqFqxyzk'))


