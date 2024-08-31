# 한국어 문장 전처리기를 구현합니다.

from konlpy.tag import Komoran
import pickle

class Preprocess :
    def __init__(self, userdic=None, word2index_dic="") : # userdic -> 사용자 정의 사전(ex. 신조어, 구어체 등)
        # 입력된 문장을 단어 인덱스 사전을 이용해 단어 시퀀스 벡터로 변환하는 기능을 추가
        # train_tools/dict/create_dict.py 작업을 수행 후 chatbot_dict.bin 파일이 생성되어야 함
        if (word2index_dic != "") :
            f = open(word2index_dic, "rb")
            self.word_index = pickle.load(f)
            f.close()
        else :
            self.word_index = None
        
        # komoran의 형태소 분석기를 초기화 한다.
        self.komoran = Komoran(userdic=userdic)
        
        # Komoran 형태소 분석기로 형태소를 쪼갠 후, 제외할 필요없는 품사 지정
        self.exclusion_tags = [
            # 각 tag가 의미하는 품사는 아래 웹페이지에서 확인 할 수 있다.
            # https://docs.komoran.kr/firststep/postypes.html
            'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ',
            'JX', 'JC',
            'SF', 'SP', 'SS', 'SE', 'SO',
            'EP', 'EF', 'EC', 'ETN', 'ETM',
            'XSN', 'XSV', 'XSA'
        ]
        
    '''
    Komoran 형태소 분석기의 POS 태거를 호출하는 메서드 정의
    Preprocess 클래스 외부에서는 Komoran 형태소 분석기 객체를 
    직접적으로 호출할 일이 없게 하기 위해 정의한 wrapper function.
    (형태소 분석기 종류를 바꾸게 될 경우 이 wrapper function 내용만 변경하면 된다.)
    '''
    def pos(self, sentence) :
        return self.komoran.pos(sentence) # 한국어 문장을 형태소 분석
        # 반환결과 -> [(형태소, 태그), .....]
    
    def get_keywords(self, pos, without_tag=False) :
        f = lambda x : x in self.exclusion_tags
        word_list = []
        
        for p in pos : 
            if f(p[1]) is False : # 형태소가 제외할 품사가 아닌 경우
                word_list.append(p if without_tag is False else p[0])
        
        return word_list                
    
    
    # 키워드를 단어 인덱스 시퀀스로 변환
    def get_wordidx_sequence(self, keywords) :
        if self.word_index is None :
            return []
        
        w2i = []
        for word in keywords :
            try :
                w2i.append(self.word_index[word])
            except KeyError :
                w2i.append(self.word_index["OOV"])
                
        return w2i