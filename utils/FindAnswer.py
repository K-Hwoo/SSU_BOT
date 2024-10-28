import torch
import numpy as np
from numpy import dot
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer, util
import random

class FindAnswer :
    def __init__(self, preprocess, embedding_data, db) :
        self.p = preprocess # 텍스트 전처리기
        self.model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS") # 사전 훈련된 SBERT
        self.embedding_data = embedding_data # 임베딩 정보 데이터
        self.db = db # 연결할 데이터베이스
        
        # 인사말 리스트
        self.hello = ["안녕하세요 SSU_BOT 입니다. 만나서 반갑습니다!",
                      "안녕 나는 SSU_BOT, Version.1이어서 간단한 답변만 가능해",
                      "안녕하세요 학교 정보를 알려주는 챗봇, SSU_BOT 입니다."]
        
        # 메뉴 추천 문구 리스트
        self.recommend = ["오늘 식사는 지지고 어떠세요!",
                          "오늘 식사는 도담식당에서 하는걸로...",
                          "오늘 식사는 연래춘에서 짜장면을 먹어봅시다~"]
        
    def search(self, query, intent) :
        # return 해야할 정보
        selected_qes = None
        query_intent = None
        answer = None
        imageURL = "없음"
        score = None
        
        # 의도가 "인사"일 경우 우선 처리
        # 의도 "인사"는 테스트용 겸 의도 분류 모델의 목적을 보여주기 위해 설계 하였음
        if intent == "인사" :
            answer = self.hello[random.randint(0, 2)]
            imageURL = "http://15.164.249.147:5000/images/hello.jpg"
            score = 1.
           
            return selected_qes, query_intent, score, answer, imageURL
        
        
        # 데이터베이스 상의 질문과의 유사도 검사 후, 답변을 검색
        
        # 입력 받은 문장을 전처리 -> 형태소만 추출해서 공백없이 하나로 합치기
        pos = self.p.pos(query)
        keywords = self.p.get_keywords(pos, without_tag=True)
        query_pre = ""
        for k in keywords :
            query_pre += str(k)
            
        # 전처리된 질문을 인코딩하고 텐서화
        query_encode = self.model.encode(query_pre)
        query_tensor = torch.tensor(query_encode)
        
        # 코사인 유사도를 통해 질문 데이터 선택
        cos_sim = util.cos_sim(query_tensor, self.embedding_data)
        best_sim_idx = int(np.argmax(cos_sim))
        
        # idx는 0부터 시작, sql id는 1부터 시작
        sql = f"SELECT * FROM question_answer_pairs WHERE id={best_sim_idx+1}"
        selected = self.db.select_one(sql) # 데이터베이스에서 선택된 row
        
        selected_qes = selected["query"] 
        query_intent = selected["intent"]
        answer = selected["answer"]
        imageURL = selected["answer_image"]
        
        if query_intent == intent : # 질문 의도 분석한 결과와 실제 의도가 맞을 때
            # 데이터베이스에서 선택한 질문 인코딩
            selected_qes_encode = self.model.encode(selected_qes)
        
            # 유사도 점수 측정
            score = dot(query_tensor, selected_qes_encode) / (norm(query_tensor) * norm(selected_qes_encode))
            
            # =============
            # 입력한 문장 의도 예측이 "메뉴"인 경우
            if intent == "메뉴" :
                if answer == "random" :
                    answer = self.recommend[random.randint(0, 2)]
                    score = 1.
           
                    return selected_qes, query_intent, score, answer, imageURL
                else : 
                    answer = "식단표 정보는 준비 중입니다 죄송합니다 (_ _)"
                    score = 1.
                    # 답변으로 가져온 웹주소에서 식단 크롤링
                    # selenium 동적 크롤링 해야해서 일단 보류
                    return selected_qes, query_intent, score, answer, imageURL
            
        else : # 질문 의도 분석한 결과와 실제 의도가 다를 때
            score = -1
            
        return selected_qes, query_intent, score, answer, imageURL
            