import socket
import threading

# connection data
FORMAT = 'utf-8'
HEADER = 1024
PORT = 5050
SERVER = '192.168.1.114'
DISCONNECT_MESSAGE = '/DISCONNECT!'

# start server
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect((SERVER,PORT))

# ask for user name
userName = input('Enter your name please: ')

# listening to the server
def receive():
    # start by geting the username if the server sends '-NAME-'
    if server.recv(HEADER).decode(FORMAT) == '-NAME-':
        server.send(userName.encode(FORMAT))
    while True:
        # receive the messages
        msg = server.recv(HEADER).decode(FORMAT)
    
        # if the server sends the [DISCONNECT_MESSAGE]
        # then then break out of the [receive] thread
        if msg == DISCONNECT_MESSAGE:
            print(msg)
            break

        # print the messages
        print(msg)

# sending to the server
def write():
    global connected
    while True:
        msg = '{}'.format(input(''))
        server.send(msg.encode(FORMAT))
        
        # if the entered message is th [DISCONNECT_MESSAGE]
        # then break out of the [write] thread
        if msg == DISCONNECT_MESSAGE:
            break

# start threads for receining
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# start threads for writing
write_thread = threading.Thread(target=write)
write_thread.start()
