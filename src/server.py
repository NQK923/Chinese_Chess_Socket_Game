import socket
import threading
import pickle

PORT = 5050
DISCONNECTMESSAGE = "!disconnect"
SERVER = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (SERVER, PORT)
server.bind(ADDR)

BoardData = None
chessPlayer = []

def handle_client(socketNumber, address, ID):
    print(f"{address} player connected")
    connected = True
    while connected:
        try:
            data = socketNumber.recv(4098)
            if data:
                chessPlayer[(1+ID) % 2].send(data)
                print(pickle.loads(data))
            else:
                connected = False
        except:
            connected = False
    try:
        chessPlayer[(1+ID) % 2].send(pickle.dumps({"disconnect": True}))
    except:
        pass

    socketNumber.close()
    chessPlayer.remove(socketNumber)
    print(f"{address} player disconnected")

def start():
    global counter
    counter = 0
    print("server started running, address is ", SERVER)
    server.listen()
    while True:
        clientSocketNumber, addr = server.accept()
        if len(chessPlayer) < 2:
            chessPlayer.append(clientSocketNumber)
            if len(chessPlayer) == 2:
                for i in range(len(chessPlayer)):
                    chessPlayer[i].send(str(i).encode())
            thread = threading.Thread(target=handle_client, args=(clientSocketNumber, addr, counter))
            thread.start()
            counter += 1
            print(f"{counter} connections active")

start()
