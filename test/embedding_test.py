import torch
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")
embedding_data = torch.load("train_tools/qna/embedding_data.pt", weights_only=True)
df = pd.read_excel("train_tools/qna/answer_data.xlsx")

sentence = "기숙사 장소 안내해줘"
print(f"질문 문장 : {sentence}")
sentence = sentence.replace(" ", "")
print(f"공백 제거 문장 : {sentence}")

sentence_encode = model.encode(sentence)
sentence_tensor = torch.tensor(sentence_encode)

cos_sim = util.cos_sim(sentence_tensor, embedding_data)
print(f"가장 높은 코사인 유사도 idx : {int(np.argmax(cos_sim))}")

best_sim_idx = int(np.argmax(cos_sim))
selected_qes = df["질문(Query)"][best_sim_idx]
print(f"선택된 질문 : {selected_qes}")

selected_qes_encode = model.encode(selected_qes)

score = np.dot(sentence_tensor, selected_qes_encode) / (np.linalg.norm(sentence_tensor) * np.linalg.norm(selected_qes_encode))
print(f"선택된 질문과의 유사도 = {score}")

answer = df["답변(Answer)"][best_sim_idx]
imageURL = df["답변 이미지"][best_sim_idx]
print(f"\n답변 : {answer} \n")
print(f"답변 이미지 : {imageURL}")