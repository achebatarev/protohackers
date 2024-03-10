import multiprocessing
import socket
from main import Server, HOST, PORT, parse_input, PriceTracker, Price
import pytest

@pytest.fixture
def launch_server():
    server = Server()
    process = multiprocessing.Process(target=server.start, daemon=True)
    process.start()
    
@pytest.mark.usefixtures("launch_server")
def test_server_insert():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    data = bytes.fromhex('490000303900000065')
    client.send(data)

    assert client.recv(4096) == b'success'

def test_parse_input():
    a, b = 1000, 100_000
    data = b'Q' + a.to_bytes(4) + b.to_bytes(4)
    assert parse_input(data) == ('Q', 1000, 100_000)

def test_parse_negative_input():
    a, b = 1000, -100_000
    data = b'Q' + a.to_bytes(4, signed=True) + b.to_bytes(4, signed=True)
    assert parse_input(data) == ('Q', 1000, -100_000)

def test_insert_query():
    pt = PriceTracker()
    timestamp, price = 1000, 100_000
    pt.insert(timestamp, price)
    assert pt.data == [Price(timestamp=timestamp, price=price)]

    pt.insert(timestamp+1, price+1)
    assert pt.data == [Price(timestamp=timestamp, price=price), Price(timestamp=timestamp+1, price=price+1)]

def test_find_mean_query():
    pt = PriceTracker()
    pt.data = [Price(1000, 100_000), Price(1001, 200_000), Price(100, 5), Price(3000, 25), Price(900, 100_000)]
    assert pt.avg_query(800, 1200) == 400_000 // 3 


