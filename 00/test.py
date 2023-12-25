import multiprocessing
import socket
from main import Server, HOST, PORT
import pytest
import multiprocessing

@pytest.fixture
def launch_server():
    server = Server()
    process = multiprocessing.Process(target=server.start, daemon=True)
    process.start()
    

@pytest.mark.usefixtures("launch_server")
def test_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    data = "Hello, World"
    client.send(data.encode())
    assert client.recv(4096).decode() == data
