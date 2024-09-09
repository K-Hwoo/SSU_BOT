import socket
import json

# 챗봇 엔진 서버 접속 정보
host = "127.0.0.1" # 챗봇 엔진 서버 IP 주소
port = 5050 # 챗봇 엔진 서버 통신 포트

while True :
    print("질문 : ")
    query = input()
    if (query == "exit") :
        exit(0)
    print("-" * 40)
    
    mySocket = socket.socket()
    mySocket.connect((host, port))
    
    json_data = {
        "Query" : query,
        "BotType" : "MyService"
    }
    
    message = json.dumps(json_data)
    mySocket.send(message.encode())
    
    
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)
    print("답변 : ")
    print(ret_data["Answer"])
    print("\n")
    
mySocket.close()