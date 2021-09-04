import socket
import threading

# connection data
FORMAT = 'utf-8'
HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
DiSCONNECT_MESSAGE = '/DISCONNECT!'

# starting server
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((SERVER,PORT))
server.listen()
print(f'[SERVER IS LISTENING] wating for connections...')

# list for clients and ther usernames
clients = []
userNames = []

# broadcast message
def broadcast(msg):
    for client in clients:
        client.send(msg.encode(FORMAT))

# handle client
def handle(client,address):
    name = clients.index(client)
    print(f'[HAS BEING HANDLED] {userNames[name]} , {address}')
    while True:
        try:
            msg = client.recv(HEADER).decode(FORMAT)

            # new
            if msg == DiSCONNECT_MESSAGE:
                print(f'[HAS LEFT] {userNames[name]}')
                client.send(DiSCONNECT_MESSAGE.encode(FORMAT))
                userNames.remove(userNames[name])
                clients.remove(client)
                break   
            elif msg:
                broadcast(f'{userNames[name]}:{msg}')
        except:
            userNames.remove(userNames[name])
            clients.remove(client)
            break

# receive connections
def receive():
    while True:
        # accept connection
        client,address = server.accept()
        print(f'[{address}] has connected..')

        # request and store username
        client.send('-NAME-'.encode(FORMAT))
        userName = client.recv(HEADER).decode(FORMAT)
        userNames.append(userName)
        clients.append(client)
        
        # notifi the clients with the new user by ther username
        print(f'[USERNAME] {userName}')
        broadcast(f'{userName} joind!')
        client.send('connected to the server'.encode(FORMAT))

        # start handling the clients
        thread = threading.Thread(target=handle,args=(client,address))
        thread.start()

receive()

# 1-make rooming seystem
# by creating alist of rooms like the clients and thir usernames 
# and maybi create a dict so that evry client must have a value like a room id

# 2-login/authenication system

# 3-add a database sql/mongo-db
