import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from Preprocess import Preprocess
sys.path.append(os.path.join(os.path.dirname(__file__), '../models/intent'))
from IntentModel import IntentModel

p = Preprocess(word2index_dic='train_tools/dict/chatbot_dict.bin',
               userdic='utils/user_dic.tsv')

intent = IntentModel(model_name='models/intent/intent_model.h5', preprocess=p)

queries = [
            '언론홍보 과사무실 전화번호 뭐야',
            '회계팀 전화번호 알려줘',
            '공학관 위치 어디야?',
            '도서관 위치 알려줘.',
            '수강 신청 일정이 궁금해',
            '졸업식이 언제야',
            '도담식당 점심메뉴 알려줘',
            '오늘 점심 식사 추천',
            '기숙사 장소 안내해줘'
          ]

for query in queries :
    predict = intent.predict_class(query)
    predict_label = intent.labels[predict]
    
    print("="*30)
    print(query)
    print("의도 예측 클래스 : ", predict)
    print("의도 예측 레이블 : ", predict_label)
    print("="*30)
    