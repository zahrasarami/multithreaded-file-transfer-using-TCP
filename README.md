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
git clone 
```
## Usage
1- run `peer.py` in linux terminal .
```bash
python3 peer.py 
```
