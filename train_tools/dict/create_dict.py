"""
토크나이징 후 임베딩을 위한 단어 사전 구축
"""
    
import sys, os
from tensorflow.keras import preprocessing
import pickle
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils'))
from Preprocess import Preprocess


# =======================================================================
# .txt 데이터셋 로드 함수
def read_corpus_data(filename) : # txt 데이터 가져오기
    with open(filename, "r", encoding='UTF8') as f :
        data = [line.split("\t") for line in f.read().splitlines()]
        data = data[1:]
        return data

# Data from Text
corpus_data_from_txt = read_corpus_data("datasets/filterd_corpus.txt")
# =======================================================================

# =======================================================================
# Data from CSV
movie_review_data = pd.read_csv("datasets/영화리뷰데이터.csv")
purpose_data = pd.read_csv("datasets/용도별목적대화데이터.csv")
topic_data = pd.read_csv("datasets/주제별일상대화데이터.csv")
common_sense_data = pd.read_csv("datasets/일반상식데이터.csv")

movie_review_data.dropna(inplace=True)
purpose_data.dropna(inplace=True)
topic_data.dropna(inplace=True)
common_sense_data.dropna(inplace=True)

text1 = list(movie_review_data["document"])
text2 = list(purpose_data["text"])
text3 = list(topic_data["text"])
text4 = list(common_sense_data["query"]) + list(common_sense_data["answer"])

corpus_data_from_csv = text1 + text2 + text3 + text4
# =======================================================================


# =======================================================================
# 말뭉치 데이터에서 키워드(형태소)만 추출해서 키워드 리스트 생성
p = Preprocess()
dict = []

for c_t in corpus_data_from_txt :
    pos = p.pos(c_t[1])
    for k in pos :
        dict.append(k[0])
        
for c_c in corpus_data_from_csv :
    pos = p.pos(c_c)
    for k in pos :
        dict.append(k[0])
        
# print(dict)
        
# 단어 사전 구축 (tensorflow의 Tokenizer 사용)
# 정수 인코딩 (word2index)
# 사전의 첫번째 인덱스(1)에는 OOV 사용
# OOV -> 문장을 정수 인코딩 했을 때, 사전에 매칭되는 단어(형태소)가 없을 때 1로 인코딩됨

# 단어 사전에 포함되는 단어 수를 출현 빈도순의 100,000개 단어로 제한
tokenizer = preprocessing.text.Tokenizer(oov_token="OOV", num_words=100000)
tokenizer.fit_on_texts(dict)

word_index = tokenizer.word_index
print(f"Found {len(word_index)} unique tokens.")

f = open("train_tools/dict/chatbot_dict.bin", "wb")
try :
    pickle.dump(word_index, f)
except Exception as e :
    print(e)
finally :
    f.close() 
# =======================================================================