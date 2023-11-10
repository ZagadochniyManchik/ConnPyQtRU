import pickle
import socket


class ServerObject:
    def __init__(self):
        self.static_data = None
        self.data = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_with(self):
        self.server.connect(('127.0.0.1', 25565))

    def close_with(self):
        self.request(pencode('None') + b'<END>' + pencode('<CLOSE-CONNECTION>') + b'<END>')

    def listen_for(self):
        while True:
            data = self.server.recv(1024)
            if data == b'<NOTIFICATION-MESSAGE>':
                data = self.server.recv(1024)
                break
        return data

    def request(self, data):
        self.server.send(data)

    def receive(self):
        # self.data = b''
        # while True:
        #     self.data += self.server.recv(1024)
        #     if self.data[-13:] == b'<END-MESSAGE>':
        #         break
        return pdecode(self.server.recv(2048))


def pencode(data):
    return pickle.dumps(data)


def pdecode(data):
    return pickle.loads(data)
