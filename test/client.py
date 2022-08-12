import socket
import sys
import threading

class Client(object):
    def __init__(self,host,port):
        import logging
        self.logger = logging.getLogger("client")
        self.host = host
        self.port = port

    def start(self):
        self.logger.debug("connect to server")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        data = "some data"
        self.socket.sendall(data.encode('utf-8'))
        self.receive()
        #thread = threading.Thread(target=self.receive)
        #thread.dameon = True
        #thread.start()
        
    def close(self):
        self.socket.close()

    def receive(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                self.logger.debug(message)
            except:
                self.close()
        

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    client = Client('localhost', 9000)
    try:
        logging.info("client....")
        client.start()
    except KeyboardInterrupt:
        client.close()
        sys.exit()
    #finally:
        #client.close()
        #terminate_flag.set()
    logging.info("all done")

