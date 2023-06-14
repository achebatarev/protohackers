import socket
import threading
import logging

logging.basicConfig(level=logging.DEBUG)
HOST = '0.0.0.0'
PORT = 21234

def handler(conn: socket.socket, addr: tuple[str, int], thread_name: str):
    global i 
    with conn:
        logging.info(f"Connection with {addr} established on thread {thread_name}")
        while True: 
            data = conn.recv(1024)

            if not data:
                break

            conn.sendall(data)
        logging.info(f"Connection with {addr} on thread {thread_name} closed")
        i -= 1

if __name__ == '__main__':

    address = (HOST, PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(address)

        s.listen(5)
        i = 1
        while True:
            conn, addr = s.accept()
            thread_name = f't{i}'
            i += 1
            t = threading.Thread(target=handler, args=(conn, addr, thread_name))
            t.start()





