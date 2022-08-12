import socket
import sys
import threading


def handle(connection , address):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("address-%r" % (address,))

    try:
        logger.debug("Connected to %r", address)
        while True:
            data = connection.recv(1024).decode('utf-8')
            if data == "":
                logger.debug("no data socket closed!!")
                break
            logger.debug("data received %r", data)
            connection.sendall("Hi client ".encode('utf-8'))
            logger.debug("sent data")
    except:
        logger.exception("connection problem")
    finally:
        logger.debug("closing socket")
        connection.close()

class Server(object):
    def __init__(self, host, port):
        import logging
        self.logger = logging.getLogger("server")
        self.host = host
        self.port = port

    def start(self):
        self.logger.debug("Listening...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        
        while True:
            conn, address = self.socket.accept()
            self.logger.debug("New Connection!")
            thread = threading.Thread(target=handle, args=(conn, address))
            thread.daemon = True
            thread.start()
            thread.join()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    server = Server("0.0.0.0", 9000)
    try:
        logging.info("starting server...")
        server.start()
    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        logging.info("closing...")
        terminate_flag = threading.Event()
        logging.info("shutting down ....")
        terminate_flag.set()

        
    logging.info("all done")
