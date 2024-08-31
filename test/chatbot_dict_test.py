import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from Preprocess import Preprocess
import pickle

f = open("train_tools/dict/chatbot_dict.bin", "rb")
word_index = pickle.load(f)
f.close()

sentence = "내일 학교 가면 뭐 먹냐... 누가 점심 메뉴 추천좀 해줘."

p = Preprocess(userdic="utils/user_dic.tsv")

pos = p.pos(sentence)

keywords = p.get_keywords(pos, without_tag=True)
for word in keywords :
    try :
        print(word, word_index[word])
    except KeyError :
        print(word, word_index["OOV"])