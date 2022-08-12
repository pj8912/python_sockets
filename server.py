import socket
import sys
import time
import threading



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
            
       
            elif message == "alive":
                print(f"Client {str(address)} is {message}")
                if client not in clients:
                    clients.append(client)
            
            #else:
             #   print(f"Client {str(address)} says {message}")
            
        except:
            sys.exit(0)



def receive():
    while True:
        client, address = sock.accept()
        print('-----------------------------')
        print('New Connection :'+ str(address))
        print('-----------------------------')
        clients.append(client)
        
        client.send("You are connected to the server".encode('utf-8'))
        try:
            thread = threading.Thread(target=handle, args=(client, address))
            thread.daemon = True
            thread.start()
        except:
            print("Cannot make thread connection")


print("server running...")


def main():
    try:
        receive()
    
    except KeyboardInterrupt:
        print("closing server")        
        sys.exit(0)

if __name__ == '__main__':
   
    main()

