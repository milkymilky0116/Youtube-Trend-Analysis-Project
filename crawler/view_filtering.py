import re
view_count=['조회수 28만회', '조회수 3.2만회', '조회수 8.3천회']

def string_int_filtering(text):
    text_count = re.findall(r'(\d+(?:\.\d+)?)',text)
    int_count=float(text_count[0])
    if text.find('만')!=-1:
        int_count=int_count*10000
    elif text.find('천')!=-1:
        int_count=int_count*1000
    return int(int_count)
    
for i in range(len(view_count)):
    text=view_count[i]
    print(string_int_filtering(text))