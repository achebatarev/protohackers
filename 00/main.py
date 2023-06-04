import socket
import threading

#host = socket.gethostname()
host = 'localhost'
port = 21234
address = (host, port)

def magic(conn):
    with conn:
        print(f"I am printing here, and you have connected {addr}")
        all_data = []
        data = conn.recv(1024)
        all_data.append(data)

        conn.sendall(b''.join(all_data))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(address)

    s.listen(5)
    while True:
        conn, addr = s.accept()
        print(f'accepted {addr}')
        t = threading.Thread(target=magic, args=(conn,))
        t.start()





