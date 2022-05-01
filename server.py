from binascii import b2a_base64
import socket
import threading
from rsa import Encryption


class Server:

    def __init__(self, port: int,) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.serverkeys = Encryption()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)
        # generate keys ...

        pubs1, pubs2 = self.serverkeys.exchange()
        self.serverkeys.set_exchanged(pubs1,pubs2)
        while True:
            c, addr = self.s.accept()
            user_info = c.recv(1024).decode()
            user_info = user_info.split(',')
            username = user_info[0]
            pubu1 = user_info[1]
            pubu2 = user_info[2]
            client = Encryption()
            server_info = pubs1+','+pubs2
            c.send(server_info.encode())
            client.set_exchanged(pubu1, pubu2)
            self.username_lookup[c] = (username, client)
            self.clients.append(c)
            print(f'user {username} connected')
            threading.Thread(target=self.handle_client,
                             args=(c, addr,)).start()

    def handle_client(self, c: socket, addr):
        while True:
            msg = c.recv(1024).decode()
            if msg[-1] == '|':
                msg = msg[:-1]
                splt = msg.split(',')
                hashs, msg = splt[0], splt[1] 
                msg = self.serverkeys.decode(msg)
                hash_decoded= self.serverkeys.hash(msg)
                if hashs!=hash_decoded:
                    raise AttributeError
                else:
                    print('message not changed')
            for client in self.clients:
                final = self.username_lookup[client][1].encode(msg)
                if client != c:
                    client.send(final.encode())
                    self.username_lookup[client][1].clear_encode()
            self.serverkeys.clear_decode()
if __name__ == "__main__":
    s = Server(9001)
    s.start()
