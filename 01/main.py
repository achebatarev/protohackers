from functools import cached_property
import socket
import threading
import logging
from typing import Literal
from pydantic import BaseModel, Field, StrictFloat, computed_field, StrictFloat, StrictInt


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

HOST = '0.0.0.0'
PORT = 21234

class Request(BaseModel):
    method: Literal['isPrime'] = Field(...)
    number: StrictInt | StrictFloat = Field()

    @computed_field
    @cached_property
    def prime(self) -> bool:
        if isinstance(self.number, float):
            return False
        return is_prime(self.number)



class Response(BaseModel):
    method: str


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
            data = b''
            while True: 
                data += conn.recv(100024) 
                 
                if not data:
                    break

                logger.info(f"received request, {data}")

                requests = data.split(b'\n')[:-1]
                data = data.split(b'\n')[-1]
                response = b''.join(process_prime_request(r) for r in requests)

                logger.info(f"sending response, {response}")

                conn.sendall(response) 
                if response == b'{}':
                    break

        logging.info(f"Connection with {addr} on thread {thread_name} closed")
        self.i -= 1

def is_prime(v: int) -> bool:
    if v <= 1:
        return False
    i = 2
    while i*i <= v:
        if v%i == 0:
            return False
        i += 1
    return True 

def process_prime_request(request: bytes) -> bytes:
    #logger.info(f"processing request, {request}")
    try:
        req_obj = Request.parse_raw(request)
        return req_obj.model_dump_json(exclude={"number"}).encode() + b'\n'
    except Exception:
        return b'{}\n'



if __name__ == '__main__':
    server = Server()
    server.start()





