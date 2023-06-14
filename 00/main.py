import socket
import threading

host = '0.0.0.0'
port = 21234
address = (host, port)

def magic(conn: socket.socket):
    with conn:
        print(f"Connection with {addr} established")
        while True: 
            data = conn.recv(1024)

            if not data:
                break

            conn.sendall(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(address)

    s.listen(5)
    while True:
        conn, addr = s.accept()
        print(f'accepted {addr}')
        t = threading.Thread(target=magic, args=(conn,))
        t.start()





