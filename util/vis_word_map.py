from pyvis.network import Network
from gensim.models import KeyedVectors
import pandas as pd
import operator

net=Network(height='1200px', width='900px',bgcolor='#222222', font_color='white')
net.barnes_hut()
df=pd.read_csv('util/edge_data.csv')
model_name='util/post.embedding'
model=KeyedVectors.load(model_name)

model_lib=model.wv
vocab=model.wv.key_to_index
tmp=[]
node=[]
def get_src():
    return list(df['src'])

def search_word(result):
    for i in range(len(result)):
        tmp_result=__search_word(result[i])
        node.append(tmp_result)

def __search_word(word):
    
    similar_word=df[df['src']==word]
    tmp_result=list(similar_word['dst'])
    for i in range(len(tmp_result)):
        if tmp_result[i] not in tmp:
            tmp.append(tmp_result[i])
    return tmp_result

def make_word_map(word):
    
    similar_words=df[df['src']==word]
    result=list(similar_words['dst'])
    tmp.append(word)
    search_word(result)
    sources=[]
    targets=[]
    weights=[]

    node_size={}

    word_similar_list=[]

    for i in range(len(tmp)):
        similarity_val=model_lib.similarity(word,tmp[i])
        word_similar_list.append(tmp[i])


    for i in range(len(word_similar_list)):
        similar_words=model_lib.similar_by_word(word_similar_list[i])
        for x,y in similar_words:
            similarity_val=model_lib.similarity(word,x)
            if similarity_val>0.7:
                sources.append(word_similar_list[i])
                targets.append(x)
                weights.append(y)

    tmp_targets=list(set(targets))
    tmp_targets.append(word)


    for i in range(len(tmp_targets)):
        similarity_val=model_lib.similarity(word,tmp_targets[i])
        node_size[tmp_targets[i]]=round(similarity_val*100)

    edge_data=zip(sources,targets,weights)

    edge_data_sort=sorted(edge_data,key= lambda t: t[2], reverse=True)



    search_list=[]
    for i in range(int(len(edge_data_sort)/3)):
        search_list.append(edge_data_sort[i][0])
    search_list=list(set(search_list))
    if word not in search_list:
        search_list.append(word)


    #return search_list


    for e in edge_data:
        src=e[0]
        dst=e[1]
        val=e[2]
        net.add_node(src,src, title=src)
        net.add_node(dst,dst, title=dst)
        net.add_edge(src,dst, value=round(val*10))
    for node in net.nodes:
        if node['id'] in tmp_targets:
            node['size']=node_size[node['id']]

make_word_map('고양이')

net.show('test.html')





