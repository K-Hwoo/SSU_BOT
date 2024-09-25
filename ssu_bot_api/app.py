from flask import Flask, request, jsonify, abort
import socket
import json
import requests
from KakaoTemplate import KakaoTemplate

# 챗봇 엔진 서버 접속 정보
host = "127.0.0.1" # 챗봇 엔진 서버 IP 주소
port = 5050 # 챗봇 엔진 서버 통신 포트

app = Flask(__name__)

def get_answer_from_engine(bottype, query) :
    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))
    
    # 챗봇 엔진 질의 요청
    json_data = {
        "Query" : query,
        "BotType" : bottype
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())
    
    # 챗봇 엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)
    
    mySocket.close()
    
    return ret_data

def send_callback_response(callback_url, response_data) :
    headers = {"Content-Type" : "application/json"}
    response = requests.post(callback_url, headers=headers, json=response_data)

    if response.status_code == 200:
        return {"result": "SUCCESS"}
    else:
        return {"result": "FAIL", "error": response.text}
    
@app.route("/query/<bot_type>", methods=["POST"])
def query(bot_type) :
    body = request.get_json()
    
    try : 
        if bot_type == "TEST" :
            # 챗봇 API 테스트용
            ret = get_answer_from_engine(bottype=bot_type, query=body["query"])
            return jsonify(ret)
        
        elif bot_type == "KAKAO" :
            # 카카오톡 스킬 처리
            body = request.get_json()
            skillTemplate = KakaoTemplate()
            
            # - 챗봇 스킬 테스트용
            # query = body["action"]["params"]["query"]
            # ret = get_answer_from_engine(bottype=bot_type, query=query)
            
            # 배포용
            callbackUrl = body["userRequest"]["callbackUrl"]
            utterance = body["userRequest"]["utterance"]
            
            try:
                ret = get_answer_from_engine(bottype=bot_type, query=utterance)
                
                response = requests.post(
                    callbackUrl,
                    json=skillTemplate.send_response(ret)
                )
                
                if response.status_code == 200:
                    print('Callback 호출 성공')
                else:
                    print(f'Callback 호출 실패: {response.status_code}, 응답 내용 : {response.text}')
            
            except Exception as error:
                print(f'Callback 호출 중 에러: {error}')       
           
            return skillTemplate.send_callback_response()
            
        # elif bot_type == "KAKAO_CB" :
        #     body = request.get_json()
        #     callbackUrl = body["userRequest"]["callbackUrl"]
        #     print(callbackUrl)
            
        #     skillTemplate = KakaoTemplate()
            
        #     return skillTemplate.send_callback_response()
     
        elif bot_type == "NAVER" :
            pass
        
        else :
            abort(404)
            
    except Exception as ex :
        abort(500)

if __name__ == "__main__" :
    app.run(host="0.0.0.0", port=5000)
    
    
    
    
    