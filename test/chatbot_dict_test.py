import sys, os
import pickle
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from Preprocess import Preprocess

# 단어 사전 바이너리 파일 로드
f = open("train_tools/dict/chatbot_dict.bin", "rb")
word_index = pickle.load(f)
f.close()

sentences = [
                "전정공 학과 사무실 전화번호 알려줘",
                "오늘 학생식당 / 학식 메뉴 뭐야",
                "졸업식 언제지? 날짜가 궁금해",
                "숭실대에 단과대는 몇 개고 전공은 뭐가 있을까?",
                "안녕 챗봇 학교 정보를 이야기 해주면 좋겠어",
            ]

p = Preprocess(userdic="utils/user_dic.tsv")

for sentence in sentences :
    print("====================\n")
    pos = p.pos(sentence)

    keywords = p.get_keywords(pos, without_tag=True)
    for word in keywords :
        try :
            print(word, word_index[word])
        except KeyError :
            print(word, word_index["OOV"])
    
    print("\n====================")