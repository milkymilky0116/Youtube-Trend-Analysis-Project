from tensorflow.keras.models import load_model
import tensorflow as tf
import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from util.sentence_tokenize import sentence_tokenize
model=keras.models.load_model('./model/predict_yt_category.model')
model.load_weights('./model/predict_yt_category.model/variables')

category_list={
    1:'Film & Animation',
    2:'Autos & Vehicles',
    10:"Music",
    15:"Pets & Animals",
    17:"Sports",
    18:"Short Movies",
    19:"Travel & Events",
    20:"Gaming",
    21:"Videoblogging",
    22:"People & Blogs",
    23:"Comedy",
    24:"Entertainment",
    25:"News & Politics",
    26:"Howto & Style",
    27:"Education",
    28:"Science & Technology",
    30:"Movies",
    31:"Anime/Animation",
    32:"Action/Adventure",
    33:"Classics",
    34:"Comedy",
    35:"Documentary",
    36:"Drama",
    37:"Family",
    38:"Foreign",
    39:"Horror",
    40:"Sci-Fi/Fantasy",
    41:"Thriller",
    42:"Shorts",
    43:"Shows",
    44:"Trailers"
}

tokenizer=Tokenizer()
test_title="당신도 프로입니까? 아이패드 프로 12.9 (5세대) 리뷰 [4K]"
token_sentence=sentence_tokenize(test_title)
encode_sentence=tokenizer.texts_to_sequences([token_sentence])
pad_sentence=pad_sequences(encode_sentence, maxlen=30)

score=model.predict(pad_sentence)
print(category_list[score.argmax()], score[0,score.argmax()])