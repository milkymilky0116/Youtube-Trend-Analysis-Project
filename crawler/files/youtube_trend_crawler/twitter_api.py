import twitter
from collections import Counter
twitter_consumer_key = "3GMcnn0TU3LJ7OzYI1l06kmdY"
twitter_consumer_secret = "ll8ZiXwfE8RPyDCHm23Mzm66XFwaXdHBpb4AojTBqGkNGQodYA"  
twitter_access_token = "1405566672522465281-8I81m6mU5VGPKBpCIsgDYFQyEvOtZw"
twitter_access_secret = "AlT8zhRYvEPxKH5uuieqbifmoj0SwN7B9tOXUpWBG7p3V"
twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                          consumer_secret=twitter_consumer_secret, 
                          access_token_key=twitter_access_token, 
                          access_token_secret=twitter_access_secret)


query='부산여행'
status=twitter_api.GetSearch(term=query,count=10)
result=[]
for item in status:
    for tag in item.hashtags:
        result.append(tag.text)

print(Counter(result).most_common(20))

