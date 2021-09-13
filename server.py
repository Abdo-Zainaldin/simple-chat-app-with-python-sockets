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

# dict for clients {client:room}
clients = {}

# dict for chat rooms {room:[list of clients]}
chat_rooms = {'0':[]}

# list for clients names
userNames = []

# disconnecting/deleting clients function
def disconnect(client):
    name = list(clients.keys()).index(client)
    userNames.pop(name)
    chat_rooms[clients[client]].remove(client)
    clients.pop(client)

# broadcast message by the room prameter
def broadcast(msg,room):
    for client in room:
        client.send(msg.encode(FORMAT))

# handle client
def handle(client,address):
    # get name of the client to print in server console
    usrer_name = userNames[list(clients.keys()).index(client)]
    print(f'[HAS BEING HANDLED] {usrer_name} , {address}')

    while True:
        try:
            # receive messages from client
            msg = client.recv(HEADER).decode(FORMAT)
            
            # get name of the client
            usrer_name = userNames[list(clients.keys()).index(client)]

            # handel the disconnect message
            if msg == DiSCONNECT_MESSAGE:
                print(f'[HAS LEFT] {usrer_name}')
                client.send(DiSCONNECT_MESSAGE.encode(FORMAT))
                disconnect(client)
                break
            # handel the '/' commands
            elif msg.startswith('/'):
                txtAfterCommand = msg.split()[1]

                # handel the '/room' command
                if msg.startswith('/room') and len(msg.split()) > 1:
                    
                    # try if the specified room existed else create a new one
                    try:
                        chat_rooms[txtAfterCommand]
                    except:
                        chat_rooms[txtAfterCommand] = []

                    # brodcast that there is a cliet has
                    broadcast(f'{usrer_name} joind!',chat_rooms[txtAfterCommand])

                    # remove the client from the main room '0'
                    chat_rooms[clients[client]].remove(client)

                    # add the clien to the new room
                    clients[client] = txtAfterCommand
                    chat_rooms[clients[client]].append(client)
                continue

            # broadcast the message to all clients with in the client room
            elif msg:
                broadcast(f'{usrer_name}:{msg}',chat_rooms[clients[client]])
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

