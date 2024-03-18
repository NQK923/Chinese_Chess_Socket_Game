import socket
import pickle

class Network:
    def __init__(self):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.port=5050
        self.ServerAddress=socket.gethostbyname(socket.gethostname())
        print("initializating now")

        self.connect()
    def connect(self):
        self.client.connect((self.ServerAddress,self.port))
        print("client is trying to connect")

    def disconnect(self):
        self.client.send("!disconnect".encode())
        self.client.close()
    def send(self,data):
        data_string = pickle.dumps(data)
        print("sending data")
        print(data)
        self.client.send(data_string)
        print(pickle.loads(data_string))
    def receiveID(self):
        data=self.client.recv(4096)
        return data
    def receive(self):
        data=self.client.recv(4096)
        return pickle.loads(data)

if __name__ == "__main__":
    n=Network()
    while True:
        print("hi i am the client")

    
        data=n.receive()
        print(data)
