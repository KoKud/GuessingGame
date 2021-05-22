import socket
import threading
import random

HEADER = 1024
PORT = 6000
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = "192.168.0.13"
print(SERVER)
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr,status, goodGame, serverAnsw, clientAnsw):
    print(f"[NEW CONNECTION] {addr} connected.")

    conn.send("CONNECTED\n".encode(FORMAT))
    myName = str(conn.recv(HEADER).decode(FORMAT))
    conn.send("WAIT\n".encode(FORMAT))
    while True:
        status[myName] = True
        while status[myName]:
            pass

        if(len(serverAnsw)>0):
            if(str(serverAnsw[myName]).split('$')[0]=="WON"):
                print(f"[{addr} : {myName}] SEND WON")
                conn.send("GOOD\n".encode(FORMAT))
            elif(str(serverAnsw[myName]).split('$')[0]=="LOSS"):
                print(f"[{addr} : {myName}] SEND LOSS")
                conn.send("WRONG\n".encode(FORMAT))
                conn.send(str(serverAnsw[myName]).split('$')[1].encode(FORMAT))

        if (goodGame[0] == True):
            conn.send("GG\n".encode(FORMAT))
            break

        conn.send("YOURDIGIT\n".encode(FORMAT))

        clientAnsw[myName]=conn.recv(HEADER).decode(FORMAT)

    conn.close()

def Game():
    server.listen()
    playerAmount=2
    print("[STARTING] server is starting... waiting for %d connections"%playerAmount)
    status = {}
    goodGame = [False]
    serverAnsw = {}
    clientAnsw = {}
    while (threading.activeCount()-1)<playerAmount:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr,status, goodGame, serverAnsw, clientAnsw))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

    while len(status) < playerAmount:
        pass

    while goodGame[0]==False:
        for x in status.keys():
            status[x] = False

        while (len(clientAnsw) < playerAmount):
            pass

        myGuess = random.randint(1, 6)
        print(f"[SERVER] My random number: {myGuess}")
        for x in clientAnsw.keys():
            if (myGuess == int(clientAnsw[x])):
                goodGame[0] = True
                serverAnsw[x] = "WON$"
            else:
                serverAnsw[x] = "LOSS$"+str(myGuess)
        clientAnsw.clear()

    for x in status.keys():
        status[x] = False

Game()