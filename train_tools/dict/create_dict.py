"""
제작 하는 chatbot engine에서 의도 분류 및 개체명 인식 모델의 학습을 하려면
"단어 사전(어휘 사전)을 구축해야 한다."
"""
    
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils'))
from Preprocess import Preprocess
from tensorflow.keras import preprocessing
import pickle
import pandas as pd

def read_corpus_data(filename) : # txt 데이터 가져오기
    with open(filename, "r", encoding='UTF8') as f :
        data = [line.split("\t") for line in f.read().splitlines()]
        data = data[1:]
        return data
        
#
movie_review_data = pd.read_csv("../../datasets/영화리뷰데이터.csv")
purpose_data = pd.read_csv("../../datasets용도별목적대화데이터.csv")
topic_data = pd.read_csv("../../datasets주제별일상대화데이터.csv")
common_sense_data = pd.read_csv("../../datasets일반상식데이터.csv")

movie_review_data.dropna(inplace=True)
purpose_data.dropna(inplace=True)
topic_data.dropna(inplace=True)
common_sense_data.dropna(inplace=True)

text1 = list(movie_review_data["document"])
text2 = list(purpose_data["text"])
text3 = list(topic_data["text"])
text4 = list(common_sense_data["query"]) + list(common_sense_data["answer"])

corpus_data_from_csv = text1 + text2 + text3 + text4

print("말뭉치 데이터(CSV) 불러오기 및 전처리 완료")
#

corpus_data_from_txt = read_corpus_data("../../datasetscorpus.txt")

# 말뭉치 데이터에서 키워드만 추출해서 사전 리스트 생성
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
        
# 사전에 사용될 word2index 생성
# 사전의 첫 번째 인덱스에는 OOV 사용

# 단어 사전에 포함되는 단어 수를 가장 많이 등장한 100,000개 단어로 제한
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