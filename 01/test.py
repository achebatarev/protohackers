import multiprocessing
import socket
from main import Server, HOST, PORT, process_prime_request, is_prime
import pytest
import multiprocessing

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@pytest.fixture(scope='session')
def launch_server():
    server = Server()
    process = multiprocessing.Process(target=server.start, daemon=True)
    process.start()
    
@pytest.mark.usefixtures("launch_server")
@pytest.mark.timeout(1)
def test_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    data = "Hello, World"
    client.send(data.encode())

@pytest.mark.usefixtures("launch_server")
@pytest.mark.timeout(1)
def test_json_valid_request():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    data = '{"method":"isPrime","number":123}\n'
    client.send(data.encode())
    assert client.recv(4096).decode() == '{"method":"isPrime","prime":false}\n'

@pytest.mark.usefixtures("launch_server")
@pytest.mark.timeout(1)
def test_json_multiple_fields_in_request():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    data = '{"method":"isPrime","number":123}\n{"method":"isPrime","number":3}\n'
    client.send(data.encode())
    assert client.recv(4096).decode() == '{"method":"isPrime","prime":false}\n{"method":"isPrime","prime":true}\n'


@pytest.mark.usefixtures("launch_server")
@pytest.mark.timeout(1)
def test_json_invalid_request():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    data = "{}\n"
    client.send(data.encode())
    assert client.recv(4096).decode() == data

def test_process_valid_prime_request_false():
    data = b'{"method":"isPrime","number":123}\n'
    assert process_prime_request(data) == b'{"method":"isPrime","prime":false}\n'

def test_process_valid_prime_request_true():
    data = b'{"method":"isPrime","number":7}\n'
    assert process_prime_request(data) == b'{"method":"isPrime","prime":true}\n'

def test_process_valid_prime_request_with_float():
    data = b'{"method":"isPrime","number":7.3}\n'
    assert process_prime_request(data) == b'{"method":"isPrime","prime":false}\n'

def test_process_different_method():
    data = b'{"method":"isNotPrime","number":7}\n'
    assert process_prime_request(data) == b"{}\n"

def test_process_invalid_prime_request():
    data = b"{hello_world}\n"
    assert process_prime_request(data) == b"{}\n"

def test_process_invalid_number_request():
    data = b'{"method":"isPrime","number":true}\n'
    assert process_prime_request(data) == b"{}\n"

@pytest.mark.parametrize("number,expected", [(-3, False), (0, False), (1, False), (2, True), (3, True), (4, False), (5, True), (7, True), (8, False)])
def test_is_prime(number, expected):
    assert is_prime(number) == expected

