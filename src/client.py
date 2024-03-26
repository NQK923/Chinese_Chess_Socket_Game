import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5050
        # Sử dụng địa chỉ localhost
        self.serverAddress = "127.0.0.1"
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
            print("Sending data:", data)
            self.client.send(data_string)
            print("Data sent successfully.")
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
    print("Hi, I am the client.")

    while True:
        data = network.receive()
        if data:
            print(data)
        else:
            print("No data received, or connection error.")
            break  # Break the loop if there's an error or no data
