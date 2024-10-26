class KakaoTemplate : 
    def __init__(self) :
        # 템플릿 버전
        self.version = "2.0"
        
    # 단순 텍스트 출력 요소
    def simpleTextComponent(self, text) :
        return {
            "simpleText" : {"text" : text}
        }
        
    # 단순 이미지 출력 요소
    def simpleImageComponent(self, imageUrl, altText) :
        return {
            "simpleImage" : {
                "imageUrl" : imageUrl,
                "altText" : altText
            }
        }
        
    # 사용자에게 응답 스킬 전송
    def send_response(self, bot_resp) :
        responseBody = {
            "version" : self.version,
            "template" : {
                "outputs" : []
            },
        }
        
        # 이미지가 텍스트보다 먼저 출력됨
        if bot_resp["AnswerImageUrl"] != "없음" :
            responseBody["template"]["outputs"].append(
                self.simpleImageComponent(bot_resp["AnswerImageUrl"], "[대체 텍스트는 준비 중입니다.]")
            )
            
        # 텍스트 답변
        if bot_resp["Answer"] is not None :
            responseBody["template"]["outputs"].append(
                self.simpleTextComponent(bot_resp["Answer"])
            )
            responseBody["template"]["outputs"].append(
                self.simpleTextComponent(
                    "★ 숭실대학교 관련 다른 정보가 궁금하다면? ★ \
                     ex) 전정공 번호 뭐야? / 교직팀 위치 알려줘 / \
                     수강신청 날짜 언제야? / 오늘 점심 메뉴 추천해줘 \
                     등으로 질문해 보세요.")
            )
            
        return responseBody
