link=['/watch?v=2ZCrTajARtI']
def convert_id(link_list):
    result=[]
    for link in link_list:
        link=link[link.find('=')+1:]
        result.append(link)
    return result
print(convert_id(link))