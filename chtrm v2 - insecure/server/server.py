import socket 
import pickle
from _thread import start_new_thread
from termcolor import colored
from database_service import verify_user, register, search_user




class user_model:
    def __init__(self, username, password):
        self.username = username
        self.password = password



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = '0.0.0.0' #first IP on this computer for every network it will connect to
Port = 6667
print(IP_address)
print(socket.gethostname())

server.bind((IP_address, Port))
server.listen(100) #maximum number of connections is 100

list_of_clients = []



#thread to handle each different client session
def clientthread(conn):
    response = pickle.loads(conn.recv(4096)) #either register or login

    if response == 'r':  #register and then redirected to a chat session
        user_obj = pickle.loads(conn.recv(4096)) #recieve user infomation as a dictionary trying to login
        user = user_model(user_obj['username'], user_obj['password']) #create a user object to use here
        if register_user(user):
            conn.send(pickle.dumps(colored('Registered','green')))

            chat_session(conn, user.username)
        else:
            conn.send(pickle.dumps(colored('Username already Exists', 'red')))
            conn.close()
            remove(conn)

    elif response == 'l': #login and join chat session
        user_obj = pickle.loads(conn.recv(2048)) #recieve user information trying to login
        name = user_obj['username']
        password = user_obj['password']
        user = user_model(name, password) #create a user object to use here

        
        if login(user):
            conn.send(pickle.dumps(colored('Logged in','green')))
            print(f'{user.username} logged in')
            
            chat_session(conn, user.username)

        else:
            conn.send(pickle.dumps(colored('Wrong username or password','red'))) 
            conn.close()
            remove(conn)
    else:
        conn.send(pickle.dumps(colored('Invalid input', 'red')))
        conn.close()
        remove(conn)



#verified chat session
def chat_session(conn, username):
    conn.send(pickle.dumps('Welcome to the chatroom!\n'))

    while True:
        try:
            message = pickle.loads(conn.recv(2048))
            if message:
                print(f'<{username}> {message}')
                message_to_send = pickle.dumps(colored(f'<{username}>  ', 'green') + message)
                broadcast(message_to_send, conn)
            else:
                remove(conn)
        except:
            print(f'{username} disconnected')
            break
        


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection: #don't send to the client that sent the message
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


def login(user):
        return verify_user(user.username, user.password)


def register_user(user):
    if search_user(user.username): #checks if the username already exists and doesn't register
        return False
    else:
        register(user.username, user.password)
        return True



#server
while True:
    try:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        print(f'{addr[0]} connected')

        start_new_thread(clientthread, (conn, )) #start a thread on the host computer for every new client connected
    except:
        continue



server.close()
