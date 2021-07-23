from gensim.models import Word2Vec, word2vec
import pandas as pd
model=word2vec.Word2Vec.load("model/post.embedding")
simillar_word=model.wv.most_similar(positive=["뉴스"])
df=pd.DataFrame(simillar_word)
print(df)
