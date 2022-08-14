import socket
import threading
import sys

class Server:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.clients = []
        self.peers = []
        

    def handle(self, client, address):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                
                if message == "dead":
                    print(f"Client {str(address)} is disconnected")
                    self.clients(client)
                    self.peers(address)

                    self.clients.close()

                elif message == "alive":
                    print(f"Client {str(address)} is {message}")
                    #print("All Clients: {}".format(self.clients))
                    print("All Peers: {}".format(str(self.peers)))

                    if client not in self.clients:
                        self.clients.append(client)


            except:
                sys.exit(0)


    def receive(self):
        while True:
            client, address = self.sock.accept()
            print('------------------------------')
            print('New Connection: '+ str(address))
            print()
            self.clients.append(client)
            self.peers.append(address)
            client.send("You are connected to the server".encode('utf-8'))
            try:
                thread = threading.Thread(target=self.handle, args=(client,address))
                thread.daemon = True
                thread.start()
            except:
                print("Cannot make thread connection..")

    def disconnect_server(self):
        self.sock.send("server_dead".encode('utf-8'))
        self.sock.close()

def main():
    server = Server('localhost', 9000)
    while True:
     try:
         print('server started...')
         server.receive()
         
     except KeyboardInterrupt:
         print("closing server..")
        
         sys.exit(0)
     except:
         print("connection error")

if __name__ == '__main__':
    main()
