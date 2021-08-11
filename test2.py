import csv

f=open('dataset/KR_videos.csv','r', encoding='utf-8')
csvReader=csv.reader(f)

for row in csvReader:
        video_info_title=(row[0])
        print(type(video_info_title))