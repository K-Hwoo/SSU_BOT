import torch
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from Preprocess import Preprocess
from Database import Database
sys.path.append(os.path.join(os.path.dirname(__file__), '../config'))
from DatabaseConfig import *

# 전처리 객체 생성
p = Preprocess(word2index_dic="train_tools/dict/chatbot_dict.bin", userdic="utils/user_dic.tsv")

# 데이버베이스 연결 객체 생성
db = Database(
    host = DB_HOST,
    user = DB_USER,
    password = DB_PASSWORD,
    db_name = DB_NAME
)
db.connect()


query = "컴공 학과 사무실 전화번호"

sys.path.append(os.path.join(os.path.dirname(__file__), '../models/intent'))
from IntentModel import IntentModel

intent = IntentModel(model_name="models/intent/intent_model.h5", preprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]


print(f"질문 : {query}")
print(f"의도파악 : {intent_name}")
print("=" * 40)


from FindAnswer import FindAnswer
embedding_data = torch.load("train_tools/qna/embedding_data.pt", weights_only=True)


f = FindAnswer(p, embedding_data, db)
selected_qes, query_intent, score, answer, imageURL = f.search(query, intent_name) 
    
if score < 0.6 : 
    print("score not enough")
    answer = "죄송합니다. 저도 잘 모르겠어요 조금 더 공부할게요 ( _ _ )"
    imageURL = "없음"

print(f"답변 : {answer}")

db.close()