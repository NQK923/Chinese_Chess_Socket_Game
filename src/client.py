
import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5050
        self.serverAddress = "192.168.174.1"
        print("Initializing now...")
        self.connect()

    def connect(self):
        try:
            self.client.connect((self.serverAddress, self.port))
            print("Client is trying to connect...")
        except socket.error as e:
            print(f"Error connecting to server: {e}")

    def disconnect(self):
        try:
            self.client.send("!disconnect".encode())
            self.client.close()
            print("Disconnected from server.")
        except socket.error as e:
            print(f"Error disconnecting from server: {e}")

    def send(self, data):
        try:
            data_string = pickle.dumps(data)
            self.client.send(data_string)
        except socket.error as e:
            print(f"Error sending data: {e}")

    def receiveID(self):
        try:
            data = self.client.recv(4096)
            return data.decode()
        except socket.error as e:
            print(f"Error receiving ID: {e}")
            return None

    def receive(self):
        try:
            data = self.client.recv(4096)
            return pickle.loads(data)
        except socket.error as e:
            print(f"Error receiving data: {e}")
            return None


if __name__ == "__main__":
    network = Network()

    while True:
        data = network.receive()
        if data:
            print(data)
        else:
            print("No data received, or connection error.")
            break
