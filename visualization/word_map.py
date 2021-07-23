from pyvis.network import Network
from gensim.models import KeyedVectors
import pandas as pd

net=Network(height='600px', width='800px',bgcolor='#222222', font_color='white')
net.barnes_hut()
model_name='post.embedding'
model=KeyedVectors.load(model_name)

model_lib=model.wv
vocab=model.wv.key_to_index

sources=[]
targets=[]
weights=[]
for word in vocab:
    similar_words=model.wv.similar_by_word(word)
    for x,y in similar_words:
        sources.append(word)
        dst=x
        val=y
        targets.append(dst)
        weights.append(val)
edge_data=zip(sources,targets,weights)
df=pd.DataFrame(edge_data, columns=['src','dst','weight'])
df.to_csv('edge_data.csv',mode='w', index=False, encoding='utf-8')

