import socket
import sys
import select
import pickle
from getpass import getpass
from termcolor import colored


exit_signal = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_name = " " #change to the host computer's name; socket.gethostname() on the host computer
IP_address = socket.gethostbyname(host_name) #might not work 
# IP_address of server's host computer on the network is the value

Port =  6667
try :client.connect((IP_address, Port))
except: 
    print(colored('Could not connect to the server','red'))
    exit()


print(colored('''\n\n..............................................................\n
..............................................................
                    CHATROOM
..............................................................\n
..............................................................\n
''','blue',attrs=['blink','bold']))

print('Type l to login or r to register')
print('/exit to exit')

while(True):
    resp = input()
    if resp == 'l' or resp =='r':
        name = input('username: ')
        password = getpass('password: ')
        user = {'username': name, 'password': password} #use a dictionary because objects create errors when recieving
        break

    elif resp == '/exit':
        exit()

    else:
        print(colored('Invalid input', 'red'))
server_response = ''
try:
    client.send(pickle.dumps(resp))
    client.send(pickle.dumps(user))
    server_response = pickle.loads(client.recv(2048))
    print(server_response)
    print('\n')
except:
    print(colored('Connection lost','red'))

if server_response == 'Logged in' or 'Registered':
    while True:
        try:
            sockets_list = [sys.stdin, client]
            read_sockets, write_socket, error_socket = select.select(sockets_list, [], []) #listen for either keyboard or socket

            for socks in read_sockets:
                if socks == client:
                    message = socks.recv(2048)
                    message = pickle.loads(message)
                    print(message)
                else:
                        message = input()
                        if message == '/exit':
                            exit_signal = True
                            break

                        client.send(pickle.dumps(message))
                        print(colored('<You>', 'yellow'),f" {message}")
                                
        except:
            print(colored('Connection lost','red'))
            break
                
        if exit_signal:
            break


client.close()
