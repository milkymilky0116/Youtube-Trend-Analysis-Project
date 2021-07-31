from gensim.models import Word2Vec, word2vec
import pandas as pd
model=word2vec.Word2Vec.load("post.embedding")
simillar_word=model.wv.most_similar(positive=["고양이"])
df=pd.DataFrame(simillar_word)
print(df)
