import socket
import threading
import time
import pickle

PORT=5050   #1024-65535
DISCONNECTMESSAGE="!disconnect"
SERVER = "192.168.1.195"

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

ADDR=(SERVER,PORT)

server.bind(ADDR) 

BoardData=None
chessPlayer=[] 
def handle_client(socketNumber,address,ID):
    print(address,"player connected")
    connected=True
    while connected:
        data=socketNumber.recv(4098)
        if data:
            chessPlayer[(1+ID)%2].send(data)
            print(pickle.loads(data))

    socketNumber.close()

counter=0
def start():
    global counter
    print("server started running, address is ",SERVER)
    server.listen() 
    while True:
        clientSocketNumber,addr=server.accept() 
        if len(chessPlayer)<3:
            chessPlayer.append(clientSocketNumber)
            if len(chessPlayer)==2:
                for i in range(len(chessPlayer)):
                    chessPlayer[i].send(str(i).encode())
            thread=threading.Thread(target=handle_client,args=(clientSocketNumber,addr,counter))
            thread.start()
            counter+=1
            print(counter)
            print("active connection",threading.activeCount()-1)
start()