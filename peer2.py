import os
import socket
import threading
from enum import Enum

IP = socket.gethostbyname(socket.gethostname())
PORT = 8009
ADDR =(IP , PORT)
FORMAT = "utf-8"
SIZE = 1024
STAT = Enum('STAT' , ['REG','CONNECT','DOWNLOAD','DISCONNECT'])
PASSWORLD = '2222'
DATA_PATH = "server_data"

def handle_client(connSocket , cAddr) :
    connSocket.send(f"{STAT.REG.name}|[PASSWORLD]".encode(FORMAT))
    validReg = False 
    while True:
        data = connSocket.recv(SIZE).decode(FORMAT).split("|")
        stat = data[0]
        if stat == 'REG' :
            inPas = data[1]
            if inPas == PASSWORLD :
                print(f"[NEW CONNECTION] {cAddr} connected.")
                sendData = STAT.CONNECT.name + '|' + "[SECCESSFUL REGISTIRATION]"
                validReg = True
            else :
                sendData = STAT.REG.name + '|' + "[UNSECCESSFUL REGISTIRATION]"
            connSocket.send(sendData.encode(FORMAT))
        if stat == 'CONNECT' and validReg==True :
            inCmd = data[1]
            if inCmd == 'HELP' :
                sendData = STAT.CONNECT.name + "|"
                sendData += "LIST: List all the files from the server.\n"
                sendData += "UPLOAD : Upload a file to the server\n"
                sendData += "DOWNLOAD: Download a file from the server\n"
                sendData += "DELETE filename: Delete a file from the server\n"
                sendData += "LOGOUT: Disconnect from the server\n"
                sendData += "HELP: List all the commands\n"

            elif inCmd == 'LOGOUT' :
                sendData = STAT.DISCONNECT.name + "|"+f"[DISCONNECT FROM {ADDR}]"
                connSocket.send(sendData.encode(FORMAT))
                break

            elif inCmd == 'LIST' :
                files = os.listdir(DATA_PATH)
                sendData = STAT.CONNECT.name + "|"
                if len(files) == 0 :
                    sendData += "The server directory is empty"
                else :
                    sendData += "\n".join(f for f in files)

            elif inCmd == 'DELETE' :
                files = os.listdir(DATA_PATH)
                sendData = STAT.CONNECT.name + "|"
                file_name = data[2]
                if len(files) == 0 :
                    sendData += "The server directory is empty"
                else:
                    if file_name in files :
                        os.system(f"rm {DATA_PATH}/{file_name}")
                        sendData += "File deleted"
                    else:
                        sendData += "File not found"
            
            elif inCmd == 'UPLOAD' :
                name = data[2]
                text = data[3]
                filepath = os.path.join(DATA_PATH , name)
                with open(filepath,"w") as f:
                    f.write(text)
                sendData = STAT.CONNECT.name + "|" + "[SECCESSFUL UPLOAD]"

            elif inCmd == 'DOWNLOAD' :    
                files = os.listdir(DATA_PATH)
                file_name = data[2]
                print(f"[DOWNLOAD] by {cAddr}")
                sendData= STAT.DOWNLOAD.name + "|"

                if len(files) == 0 :
                    sendData += 'NOTDOWNLOAD' + 'server directory is empty'
                else:
                    if file_name in files :
                        with open(f"./{DATA_PATH}/{file_name}","r") as f :
                            text = f.read()
                        sendData += 'DOWNLOAD' + "|" + file_name+ "|" +text
                    else:
                        sendData += 'NOTDOWNLOAD' + 'this file not found'

            connSocket.send(sendData.encode(FORMAT))
        if stat == 'DOWNLOAD' and validReg==True :
            print("in download")
            sendData = STAT.CONNECT.name + "|" + data[1]
            connSocket.send(sendData.encode(FORMAT))

            

    print(f"[DISCONNECTED] {cAddr} disconnected")
            

        
                

    return




def clientMode() :
    return 
def serverMode() :
    print("[STARTING] fileSharing is starting...")
    server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[LISTENING] waiting for connection...")
    while True:
        connSocket , cAddr = server.accept()
        thread = threading.Thread(target=handle_client , args=(connSocket , cAddr))
        thread.start()
    return 





cmd = input("for connection to other peers enter CONNECT:\n")
if( cmd == "CONNECT" ) :
    clientMode()
else :
    serverMode()