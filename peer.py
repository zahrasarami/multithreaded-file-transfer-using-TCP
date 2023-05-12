import os
import socket
import threading
from enum import Enum
import tkinter as tk
from tkinter import messagebox

IP = socket.gethostbyname(socket.gethostname())
PORT = 8011
ADDR =(IP , PORT)
print(ADDR)
FORMAT = "utf-8"
SIZE = 1024
STAT = Enum('STAT' , ['REG','CONNECT','DOWNLOAD','DISCONNECT'])
PASSWORLD = '1111'
DATA_PATH = "server_data"
serverWindow = tk.Tk()
serverWindow.geometry("300x400")
def handle_server(client , sAddr) :

    while True:
        
        data = client.recv(SIZE).decode(FORMAT).split('|')
        stat = data[0]
        msg = data[1]
        if stat == 'REG' :
            def on_login():
                pas = password_entry.get()
                return pas
            loginWindow = tk.Tk()
            password_label = tk.Label(loginWindow, text=f"{msg} Enter current peer passworld :")
            password_label.pack()
            password_entry = tk.Entry(loginWindow, show="*")
            password_entry.pack()
            login_button = tk.Button(loginWindow, text="Login", command=loginWindow.quit)
            login_button.pack()
            loginWindow.mainloop()
            pas = on_login()
            sendData = STAT.REG.name +"|"+ pas
            client.send(sendData.encode(FORMAT))
            loginWindow.destroy()
        elif stat == 'CONNECT' :
            connectionWindow = tk.Tk()
            title3 = tk.Label(connectionWindow,text="Enter your command(Enter HELP to see commands)")
            title3.pack()
            msg_lable = tk.Label(connectionWindow,text=f"[RESULT]:{msg}")
            msg_lable.pack()
            command_entry = tk.Entry(connectionWindow)
            command_entry.pack()
            command_button = tk.Button(connectionWindow, text="ENTER", command=connectionWindow.quit)
            command_button.pack()
            connectionWindow.mainloop()
            cmd = command_entry.get().split(" ")
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
            connectionWindow.destroy()

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
            messagebox.showerror(f"{msg}")
            break
    client.close()
    


def handle_client(connSocket , cAddr ) :
    connSocket.send(f"{STAT.REG.name}|[PASSWORLD]".encode(FORMAT))
    validReg = False 
    while True:
        data = connSocket.recv(SIZE).decode(FORMAT).split("|")
        stat = data[0]
        if stat == 'REG' :
            inPas = data[1]
            if inPas == PASSWORLD :
                serverModeLog(f"[NEW CONNECTION] {cAddr} connected.")
                
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
                serverModeLog(f"[DOWNLOAD] by {cAddr}")
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
            sendData = STAT.CONNECT.name + "|" + data[1]
            connSocket.send(sendData.encode(FORMAT))

            
    serverModeLog(f"[DISCONNECTED] {cAddr} disconnected")
        
    return

def clientMode() :
    def validate_input():
        try:
            index = int(entry1.get())
            sAddr = activeNodes[index]
            client = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
            client.connect(sAddr)
            thread = threading.Thread(target=handle_server , args=(client , sAddr))
            thread.start()
        except ValueError:
            error_label.config(text="Please enter an integer")

    window = tk.Tk()
    title1 = tk.Label(window ,text="Active nodes:")
    title1.pack()
    activeNodes = getActiveNodes()
    activeNodesLable = tk.Label(window ,text = activeNodes)
    activeNodesLable.pack()
    title2 = tk.Label(text="Enter your desired server Index number:")
    title2.pack()
    entry1 = tk.Entry(window)
    entry1.pack()
    button1 = tk.Button(window , text='ENTER', command=validate_input)
    button1.pack()
    error_label = tk.Label(window, fg="red")
    error_label.pack()
    window.mainloop()

    
    

def getActiveNodes():
    activeNodes = []
    with open("activeNode.txt" , 'r') as f :
        for line in f :
            node = line.strip().split(" ")
            activeNodes.append((node[0],int(node[1])))
    return activeNodes 


def serverModeLog( txt ) :
    lable = tk.Label(serverWindow,text=txt)
    lable.pack()  
def serverMode() :
    serverModeLog("[STARTING] fileSharing is starting...")
    server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    serverModeLog("[LISTENING] waiting for connection...")
    while True:
        connSocket , cAddr = server.accept()
        thread = threading.Thread(target=handle_client , args=(connSocket , cAddr))
        thread.start()





clientThread = threading.Thread(target= clientMode)
serverThread = threading.Thread(target= serverMode)
clientThread.start()
serverThread.start()
serverWindow.mainloop()
