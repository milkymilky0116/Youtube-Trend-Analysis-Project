import mariadb_data

def convert_resolution(res,link):
    result=[]
    for row in link:
        row=row.replace('/default.jpg','/{}default.jpg'.format(res))
        result.append(row)
    return result
df=mariadb_data.get_youtube_data(30,'video_id','video_title','thumbnail_link')
df_img=df['thumbnail_link']
df_img=df_img.values.tolist()
print(convert_resolution('max',df_img))