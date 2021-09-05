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
clients = {}
userNames = []

chat_rooms = {'0':[]}

# disconnecting/deleting clients function
def disconnect(client):
    name = list(clients.keys()).index(client)
    userNames.pop(name)
    chat_rooms[clients[client]].remove(client)
    clients.pop(client)

# broadcast message
def broadcast(msg,room):
    for client in room:
        client.send(msg.encode(FORMAT))

# handle client
def handle(client,address):
    name = list(clients.keys()).index(client)
    print(f'[HAS BEING HANDLED] {userNames[name]} , {address}')
    while True:
        try:
            msg = client.recv(HEADER).decode(FORMAT)
            
            name = list(clients.keys()).index(client)

            if msg == DiSCONNECT_MESSAGE:
                print(f'[HAS LEFT] {userNames[name]}')
                client.send(DiSCONNECT_MESSAGE.encode(FORMAT))
                disconnect(client)
                break
            elif msg.startswith('/'):
                txtAfterCommand = msg.split()[1]
                if msg.startswith('/room') and len(msg.split()) > 1:
                    try:
                        chat_rooms[txtAfterCommand]
                    except:
                        chat_rooms[txtAfterCommand] = []
                    broadcast(f'{userNames[name]} joind!',chat_rooms[txtAfterCommand])
                    chat_rooms[clients[client]].remove(client)
                    clients[client] = txtAfterCommand
                    chat_rooms[clients[client]].append(client)
                continue
            elif msg:
                broadcast(f'{userNames[name]}:{msg}',chat_rooms[clients[client]])
                # print(f'!=\nclient room = {len(chat_rooms[clients[client]])}')
                # print(f'0 room = {len(chat_rooms["0"])}')
                # print(f'lols room = {len(chat_rooms["lols"])}')
            else:
                continue
        except:
            disconnect(client)
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
        clients[client] = '0'
        chat_rooms['0'].append(client)
        
        # notifi the clients with the new user by ther username
        print(f'[USERNAME] {userName}')
        broadcast(f'{userName} joind!',chat_rooms['0'])
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
