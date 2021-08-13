
import urllib.request
import re
import json
import collections
from langdetect import detect

def sentiment_analyse(sentence_list):
    result_sentiment=[]
    for i in range(len(sentence_list)):
        sentence=sentence_list[i]
        if detect(sentence)=='ko' or detect(sentence)=='en':
            client_id = "zofo3v8hwj"
            client_secret = "uSaxHZaefo6WTQ2rwcdNJqVGnngg3QkjA10dvEw9"
            url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze";
            body={
                    'content':sentence
                }
            body=json.dumps(body)
            request = urllib.request.Request(url)
            request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
            request.add_header("X-NCP-APIGW-API-KEY",client_secret)
            request.add_header("Content-Type","application/json")
            response = urllib.request.urlopen(request, data=body.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                text=response_body.decode('utf-8')
                text=text[text.find('sentiment'):text.find('confidence')]
                sentiment_text= re.sub(r"[^a-zA-Z0-9:]","",text)
                sentiment_text=sentiment_text[sentiment_text.find(':')+1:]
                result_sentiment.append(sentiment_text)
            else:
                errcode="Error Code:" + rescode
                return errcode
    frequency=collections.Counter(result_sentiment)

    print(frequency)
    result=frequency.most_common(1)[0][0]
    result_dict={}
    for item in frequency:
        result_dict[item]=frequency[item]/len(result_sentiment)
    return result_dict

test=['너무 꿀잼 ㅋㅋㅋㅋㅋㅋㅋㅋ','웃기네 ㅋㅋㅋㅋㅋㅋㅋㅋ','아 개노잼','Thats so funny','그냥 그렇네~~']
test_result=[]
test_result.append(sentiment_analyse(test))

print(test_result)