import socket
import threading
import logging

logging.basicConfig(level=logging.DEBUG)

HOST = '0.0.0.0'
PORT = 21234


class Server:
    def __init__(self, host='0.0.0.0', port=21234):
        self.host = host
        self.port = port
        self.n_requests = 5

    def start(self):
        logging.info(f"Started server on ip={self.host}, port={self.port}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(self.n_requests)

            self.i = 1
            while True:
                conn, addr = s.accept()
                thread_name = f't{self.i}'
                t = threading.Thread(target=self.handler, args=(conn, addr, thread_name))
                self.i += 1
                t.start()

    def handler(self, conn: socket.socket, addr: tuple[str, int], thread_name: str = "t0"):
        with conn:
            logging.info(f"Connection with {addr} established on thread {thread_name}")

            while True: 
                data = conn.recv(1024)

                if not data:
                    break

                conn.sendall(data)

        logging.info(f"Connection with {addr} on thread {thread_name} closed")
        self.i -= 1



if __name__ == '__main__':
    server = Server()
    server.start()





