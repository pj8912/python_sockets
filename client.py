import socket 
import threading
import time
import sys

class Client:

    def __init__(self, host, port):
        
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((self.host, self.port))

        i_thread = threading.Thread(target=self.send_message)
        i_thread.daemon = True
        i_thread.start()

        while True:
            r_thread = threading.Thread(target=self.receive_message)
            r_thread.start()
            r_thread.join()

            data = self.receive_message()
            if not data: 
                break
            else:
                print('got server')


    def receive_message(self):
        try:
        
            data = self.sock.recv(1024)
            print(data.decode('utf-8'))

            return data
        except KeyboardInterrupt:
            self.send_disconnect_signal()


    def send_message(self):
        try:
            message = "alive"
            self.sock.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            self.send_disconnect_signal()
        
        

    def send_disconnect_signal(self):
        print("disconnected from the server...")
        self.sock.send("dead".encode('utf-8'))
        sys.exit()

    #def ping(self):
     #   time.sleep(2)
      #  self.send_message("alive")



def main():
    while True:
        try:
            client = Client('127.0.0.1', 9000)
        except KeyboardInterrupt as e:
            sys.exit(0)
        except:
            print("no server connected....")
            sys.exit()
             
if __name__ == "__main__":
    main()

