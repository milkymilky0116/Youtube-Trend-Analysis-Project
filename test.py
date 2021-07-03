from PyKomoran import *

# Komoran 객체 생성
komoran = Komoran(DEFAULT_MODEL['FULL'])

# 분석할 문장 준비
str_to_analyze = "① 대한민국은 민주공화국이다. ② 대한민국의 주권은 국민에게 있고, 모든 권력은 국민으로부터 나온다."

print(komoran.get_nouns(str_to_analyze))

print(komoran.get_morphes_by_tags(str_to_analyze, tag_list=['NNP', 'NNG', 'SF']))

print(komoran.get_plain_text(str_to_analyze))

print(komoran.get_token_list(str_to_analyze))

print(komoran.get_token_list(str_to_analyze, flatten=False))

print(komoran.get_token_list(str_to_analyze, use_pos_name=True))

print(komoran.get_list(str_to_analyze))
