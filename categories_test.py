from gensim.models import Word2Vec, word2vec
model=word2vec.Word2Vec.load("post.embedding")
print(model.wv.most_similar(positive=["먹방"]))
