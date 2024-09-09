import socket

class BotServer :
    def __init__(self, srv_port, listen_num) :
        self.port = srv_port
        self.listen = listen_num
        self.mySock = None
        
    # Socket 생성
    def create_socket(self) :
        self.mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mySock.bind(("0.0.0.0", int(self.port)))
        self.mySock.listen(int(self.listen))
        
        return self.mySock
    
    # client 대기
    def ready_for_client(self) :
        return self.mySock.accept()
    
    # socket 반환
    def get_sock(self) :
        return self.mySock