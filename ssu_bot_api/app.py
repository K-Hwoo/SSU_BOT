from flask import Flask, request, jsonify, abort, send_from_directory
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

# 이미지 서버역할도 같이
@app.route('/images/<filename>')
def serve_image(filename):
    # 'static/images' 폴더에서 파일을 제공
    return send_from_directory('static/images', filename)
    
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
            utterance = body["userRequest"]["utterance"]
            ret = get_answer_from_engine(bottype=bot_type, query=utterance)

            from KakaoTemplate import KakaoTemplate
            skillTemplate = KakaoTemplate()
            return skillTemplate.send_response(ret)
     
        elif bot_type == "NAVER" :
            pass
        
        else :
            abort(404)
            
    except Exception as ex :
        abort(500)

if __name__ == "__main__" :
    app.run(host="0.0.0.0", port=5000)
    
    
    
    
    