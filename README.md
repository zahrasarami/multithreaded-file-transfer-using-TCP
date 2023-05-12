# multithreaded-file-transfer-using-TCP
multithreaded file transfer using TCP in python .

## About The Project


This program provides file transfer services for hosts that have installed it . 

It is implemented in simple peer to peer topology so that we have the list of active peers in  `activenodes.txt` 

Each peer has it's own `server_date` directory that shares with other and multiple hosts can access the text files inside it .

It uses 2 parallel thread for its communication :
>serverMode: to handle authentication and connection requests .

>clientMode: to connect to other peers .

## Installation
```bash
git clone https://github.com/zahrasarami/multithreaded-file-transfer-using-TCP.git
```
## Usage
1- set `PORT` and `DATA_PATH` varieble in code .

2-update `activenodes.txt` with your active peers .

3- run `peer.py` in linux terminal .
```bash
python3 peer.py 
```
## Options
`LIST` : List all the files from the server

`UPLOAD filepath` : Upload a file to the server

`DOWNLOAD` : Download a file from the server

`DELETE filename` : Delete a file from the server

`LOGOUT` : Disconnect from the server

`HELP` : List all the commands
