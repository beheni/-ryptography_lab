import socket
import threading
from rsa import Encryption

class Client:
    def __init__(self, server_ip: str, port: int, username='') -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username
        self.server = None
        self.client = None

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return
        self.client = Encryption()
        self.username = input()
        pubu1, pubu2 = self.client.exchange()
        user_info = self.username+','+pubu1+','+pubu2
        self.s.send(user_info.encode())
        # self.s.send(pubu2.encode())

        # self.s.send(self.username.encode())
        self.client.set_exchanged(pubu1,pubu2)
        server_info=self.s.recv(1024).decode()
        pubs1,pubs2 = server_info.split(',')[0], server_info.split(',')[1]
        self.server = Encryption()
        self.server.set_exchanged(pubs1, pubs2)
        message_handler = threading.Thread(target=self.read_handler,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler,args=())
        input_handler.start()

    def read_handler(self): 
        while True:
            message = self.s.recv(1024).decode()
            message = message.split(',')[-1] 
            message = self.client.decode(message)
            print(f'To {self.username}: ', message)
            self.client.clear_decode()
            message=''

    def write_handler(self):
        while True:
            message = input()
            message = self.server.encode(message)+'|'
            self.s.send(message.encode())
            self.server.clear_encode()
            # print(f'message sent: {message}')

            # encrypt message with the secret key

            # ...
            # message =self.client.encode(message)

if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001)
    cl.init_connection()
