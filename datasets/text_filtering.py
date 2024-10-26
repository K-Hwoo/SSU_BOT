# corpus.txt 에 있는 말뭉치 데이터셋에서
# 특정 키워드를 가진 문장만 추출하여 filterd_corpus.txt로 저장하는 프로그램
# corpus.txt에 문장 추가 후에 필터링하여 사용 

target_file = "datasets/corpus.txt"
output_file = "datasets/filterd_corpus.txt"

keywords = [
            "학교", "학과", "일정", "교수", "학생", "전화번호", "번호", 
            "안녕", "반가", "위치", "사무실", "메뉴"
           ]

with open(target_file, 'r', encoding='utf-8') as input :
    with open(output_file, 'w', encoding='utf-8') as output :
        for line in input :
            if any(keyword in line for keyword in keywords) :
                output.write(line)