import threading
import json
import pandas as pd
import tensorflow as tf
import torch
from logging import handlers
import logging

from config.DatabaseConfig import *
from utils.Database import Database
from utils.BotServer import BotServer
from utils.Preprocess import Preprocess
from utils.FindAnswer import FindAnswer
from models.intent.IntentModel import IntentModel
from train_tools.qna.create_embedding_data import create_embedding_data
# pip install datasets --upgrade 해줘야 할 수 도 있음

# ========= log 처리 =========
# 질문 데이터셋 수집 목적

# Log 작성 포맷
LogFormatter = logging.Formatter("%(asctime)s, %(message)s")

# Logger 핸들러 
LogHandler = handlers.TimedRotatingFileHandler(filename="logs/SSU_BOT_log.log", 
                                               when="d", 
                                               interval=7,  
                                               backupCount=30, encoding="utf-8")
LogHandler.setFormatter(LogFormatter)
LogHandler.suffix = "%Y%m%d"

# ============================

# logger 세팅
Logger = logging.getLogger()
Logger.setLevel(logging.ERROR)
Logger.addHandler(LogHandler)

p = Preprocess(word2index_dic="train_tools/dict/chatbot_dict.bin", userdic="utils/user_dic.tsv")
print("\033[92mText Preprocessor is successfully loaded.\033[0m")

intent = IntentModel(model_name="models/intent/intent_model.h5", preprocess=p)
print("\033[92mIntent predict model is successfully loaded.\033[0m")

# - 질문 / 답변 데이터셋 불러오기
# df = pd.read_excel("train_tools/qna/answer_data.xlsx")
# print("\033[92m[ Qustion / Answer dataset ] is successfully loaded.\033[0m")

# - 임베딩 파일 (재)생성 및 불러오기
# print("\033[92mWaiting for making embedding file....\033[0m")
# create_embedding_data = create_embedding_data(preprocess=p, df=df)
# create_embedding_data.create_pt_file()
# print("\033[92mEmbedding file is sucessfully made.\033[0m")
embedding_data = torch.load("train_tools/qna/embedding_data.pt", weights_only=True)
print("\033[92mEmbedding file is sucessfully loaded.\033[0m")


def to_client(conn, addr, params) :
    db = params["db"]
    
    try :
        db.connect() # 데이터베이스 연결
        
        read = conn.recv(2048) # 수신 데이터가 있을 때까지 블로킹
        print("==============================")
        print(f"Connection from : {str(addr)}")
        
        if read is None or not read :
            # 클라이언트 연결이 끊어지거나 오류가 있는 경우
            print("클라이언트 연결 끊어짐")
            exit(0) # 스레드 강제 종료
            
        # json 데이터로 변환
        recv_json_data = json.loads(read.decode())
        print(f"데이터 수신 : {recv_json_data}")
        query = recv_json_data["Query"]
        
        # 의도 파악
        intent_predict = intent.predict_class(query)
        intent_name = intent.labels[intent_predict]
        
        # 답변 검색
        f = FindAnswer(p, embedding_data, db)
        selected_qes, query_intent, score, answer, imageURL = f.search(query, intent_name) 
        
        if score < 0.65 :
            answer = "적절한 질문 또는 좀 더 구체적으로 질문을 주세요.\
가이드라인을 알려 드릴게요!\
1. 번호 안내 : 숭실대 번호가 뭐야?\
2. 장소 안내 : 복사기 위치 알려줄래?\
3. 학사일정 안내 : 졸업식 일정을 알려줘\
4. 식사 : 오늘 점심 메뉴 추천좀…"

            imageURL = "없음"
            Logger.error(f"{query}, {query_intent}, {selected_qes}, {intent_name}, {score}")
            
        send_json_data_str = {
            "Query" : query,
            "Answer" : answer,
            "AnswerImageUrl" : imageURL,
            "Intent" : intent_name,
        }
        message = json.dumps(send_json_data_str)
        conn.send(message.encode())
        
    except Exception as ex :
        print(ex)
        
    finally :
        if db is not None :
            db.close()
        conn.close()
        

if __name__ == "__main__" :
    # 데이터베이스 연결 객체 생성
    db = Database(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db_name=DB_NAME
    )
    
    port = 5050
    listen = 500
    bot = BotServer(port, listen)
    bot.create_socket()
    print("[ SSU_BOT start ]")

    while True :
        conn, addr = bot.ready_for_client()
        params = {
            "db" : db
        }
        
        client = threading.Thread(target=to_client, args=(
            conn, # 클라이언트 연결 소켓
            addr, # 클라이언트 연결 주소 정보
            params # 스레드 함수 파라미터
        ))
        client.start()
            