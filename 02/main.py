from dataclasses import dataclass
import socket
import threading
import logging
from statistics import mean

logging.basicConfig(level=logging.DEBUG)

HOST = '0.0.0.0'
PORT = 21234

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
            pt = PriceTracker()
            while True: 
                data = conn.recv(9)

                if not data:
                    break

                logger.info(f"received request, {data}")

                try: 
                    op, a, b = parse_input(data)
                except Exception:
                    logging.error("Can't parse data")
                    conn.sendall(b'undefined')
                    break

                response: bytes = data

                if op == 'I':
                    pt.insert(a, b)
                    response = b'success'
                elif op == 'Q':
                    response = pt.avg_query(a, b).to_bytes(4)
                else:
                    logger.error("You have provided unsuported type")
                    response = b'undefined'

                conn.sendall(response)

                logger.info(f"sending response, {response}")

        logging.info(f"Connection with {addr} on thread {thread_name} closed")
        self.i -= 1

def parse_input(s: bytes) -> tuple[str, int, int]:
    _type = chr(s[0])
    int32_1 = int.from_bytes(s[1:5], signed=True)
    int32_2 = int.from_bytes(s[5:9], signed=True)
    return (_type, int32_1, int32_2)

@dataclass
class Price:
    timestamp: int
    price: int
    

# Create PriceTracker per session
class PriceTracker:
    def __init__(self):
        self.data = []

    def insert(self, timestamp: int, price: int):
        self.data.append(Price(timestamp=timestamp, price=price))

    def avg_query(self, mintime: int, maxtime: int) -> int :
        try:
            return round(mean(e.price for e in self.data if mintime <= e.timestamp <= maxtime))
        except Exception:
            return 0
        



if __name__ == '__main__':
    server = Server()
    server.start()





