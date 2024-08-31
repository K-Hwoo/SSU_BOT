import sys, os
# 현재 파일의 경로를 기준으로 상위 디렉터리로 이동하여 
# 'chatbot/utils' 경로를 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

# utils/Preprocess 모듈을 임포트할 수 있습니다.
from Preprocess import Preprocess

sentence = "내일 숭실대학교 도담식당 학식 메뉴 알려줘~"

p = Preprocess(userdic="utils/user_dic.tsv")

pos = p.pos(sentence)
ret = p.get_keywords(pos, without_tag=False)
print(ret)

ret = p.get_keywords(pos, without_tag=True)
print(ret)