import socket
import sys
import time
import threading
from queue import Queue
import traceback



host = 'localhost'
port = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen()

clients = []


def handle(client, address):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "dead":
                print(f"Client {str(address)} is disconnected")
                clients.remove(client)
                client.close()
                sys.exit(0)
            elif message == "alive":
                #print(f"Client {str(address)} is {message}")
                if client not in clients:
                    clients.append(client)
                else:
                    pass
            else:
                print(f"Client {str(address)} says {message}")
            
        except:
            #clients.remove(client)
            print(f"Client {address} disconnected")
            client.close()
            sys.exit(0)

def receive():
    while True:
        client, address = sock.accept()
        print('-----------------------------')
        print('New Connection :'+ str(address))
        print('-----------------------------')

        clients.append(client)
        client.send("You are connected to the server".encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client, address))
        thread.daemon = True
        thread.start()
        #thread.join()


print("server running...")


def main():
    

    try:
        receive()
    except KeyboardInterrupt:
        print("closing server")
        sock.close()
        sys.exit(0)
    #except Exception:
     #   traceback.print_exec(file=sys.stdout)
    sys.exit(0)

main()



   
#with client:
# while True:
#data = client.recv(1024)
#if not data:                break'''
