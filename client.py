import socket
import sys
import time
import threading
import traceback
import hashlib
import json


host = 'localhost'
port = 9000


class Client:
    def __init__(self, host, port): 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def generate_id(self):
        val = str(self.host)+str(self.port)
        id = hashlib.sha1(val.encode('utf-8'))
        id = id.hexdigest()
        scale = 16
        bits = 8
        id_in_bin = bin(int(id,scale))[2:].zfill(bits)
        return id_in_bin


    def start(self):
        while True:
            self.sock.connect((host,port))
            receive_thread = threading.Thread(target=self.receive)
            receive_thread.daemon = True
            receive_thread.start()
            info = {
                    "host":self.host,
                    "port":str(sel.port),
                    "id": self.generate_id()
            }
        
            self.ping()

    def write(self, message):
        message = message.encode('utf-8')
        self.sock.send(message)

    def stop(self):
        self.sock.close()

    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                print(message)
            except ConnectionAbortedError:
                pass
            except:
                print("Error")
                self.sock.close()
                sys.exit(0)

    def ping(self):
        while True:
            time.sleep(2)
            self.write("alive")


client = Client(host, port)

def main(client):
    try:
        client.start()
        #client = Client(host,port)
    except KeyboardInterrupt:
        print("Disconnection from server")
        client.write('dead')
        client.stop()
        sys.exit(0)
    #except Exception:
     #   traceback.print_exc(file=sys.stdout)
    sys.exit(0)

main(client)

