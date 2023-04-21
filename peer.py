import os
import socket
import threading
from enum import Enum

FORMAT = "utf-8"
SIZE = 1024
STAT = Enum('STAT' , ['REG','CONNECT','DOWNLOAD','DISCONNECT'])
DATA_PATH = "server_data2"


def clientMode() :
    activeNodes = getActiveNodes()
    sAddr = choose_peer(activeNodes)
    sIp , sPort = sAddr
    print(sAddr)
    client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    client.connect(sAddr)
    while True:
        data = client.recv(SIZE).decode(FORMAT).split('|')
        stat = data[0]
        msg = data[1]
        if stat == 'REG' :
            pas = input(f"{msg} Enter current peer passworld :")
            sendData = STAT.REG.name +"|"+ pas
            client.send(sendData.encode(FORMAT))
        elif stat == 'CONNECT' :
            print(f"{msg}")
            print("Enter your command...Enter HELP to see commands")
            cmd = input("> ").split(" ")
            print(cmd[0])
            if cmd[0] == 'HELP' :
                sendData = STAT.CONNECT.name +"|"+ 'HELP'
                
            elif cmd[0] == 'LOGOUT' :
                sendData = STAT.CONNECT.name +"|"+ "LOGOUT"
                
            elif cmd[0] == 'LIST' :
                sendData = STAT.CONNECT.name +"|"+ 'LIST'
                
            elif cmd[0] == 'DELETE' :
                sendData = STAT.CONNECT.name +"|"+ 'DELETE' +"|"+cmd[1]

            elif cmd[0] == 'UPLOAD' :
                path = cmd[1]
                with open(f"{path}","r") as f :
                    text = f.read()
                file_name = path.split("/")[-1]
                sendData= STAT.CONNECT.name + "|" + 'UPLOAD' + "|" + file_name+ "|" +text

            elif cmd[0] == 'DOWNLOAD' :
                sendData = STAT.CONNECT.name +"|"+ 'DOWNLOAD' +"|"+cmd[1]

            client.send(sendData.encode(FORMAT))
        elif stat == 'DOWNLOAD' :
            sendData = STAT.DOWNLOAD.name + "|"
            if msg == 'DOWNLOAD':
                name = data[2]
                text = data[3]
                filepath = os.path.join(DATA_PATH , name)
                with open(filepath,"w") as f:
                    f.write(text)
                sendData += f"[SECCESSFUL DOWNLOAD] {name} downloaded"
            elif msg == 'NOTDOWNLOAD':
                sendData += f"[UNSECCESSFUL DOWNLOAD]{data[2]}"
            client.send(sendData.encode(FORMAT))
        elif stat == 'DISCONNECT' :
            print(f"{msg}")
            break
    client.close()
        

    
    
def getActiveNodes():
    activeNodes = []
    with open("activeNode.txt" , 'r') as f :
        for line in f :
            node = line.strip().split(" ")
            activeNodes.append((node[0],int(node[1])))
    return activeNodes 

def choose_peer(activeNodes) :
    print(activeNodes)
    hNum = int(input("choose host:\n"))
    return activeNodes[hNum-1]
    
def serverMode() :
    return 

cmd = input("for connection to other peers enter CONNECT:\n")
if( cmd == "CONNECT" ) :
    clientMode()
else :
    serverMode()

