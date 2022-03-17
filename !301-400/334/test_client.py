import time
from multiprocessing import Process
from hashlib import sha256
from secrets import token_bytes
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR

import pytest

from client import socket_client

SERVER_MESSAGE_LENGTH = 500
SERVER_SOCKET_TIMEOUT = 1
PROCESS_SLEEP_TIME = 0.1


def do_server_operation(socket_for_incoming_connection):
    data = token_bytes(SERVER_MESSAGE_LENGTH)
    socket_for_incoming_connection.sendall(data)
    expected_response = sha256(data).digest()

    response = socket_for_incoming_connection.recv(32)

    assert expected_response == response, "Incorrect response."


def start_client(address):
    # To give server time to start before client.
    time.sleep(PROCESS_SLEEP_TIME)
    socket_client(address, SERVER_MESSAGE_LENGTH)


@pytest.fixture
def server_socket():
    with socket(AF_INET, SOCK_STREAM) as server_socket:

        for port in range(49_152, 65_535):
            server_address = ("localhost", port)
            try:
                server_socket.bind(server_address)
                break
            except OSError:
                # Port is already in use.
                continue
        else:
            raise Exception("Unable to assign port to the server. Test setup problem.")

        server_socket.settimeout(SERVER_SOCKET_TIMEOUT)
        server_socket.listen()

        yield server_socket


@pytest.fixture
def connected_client(server_socket):
    client_process = Process(target=start_client, args=(server_socket.getsockname(),))
    client_process.start()

    socket_for_incoming_connection, client_address = server_socket.accept()
    socket_for_incoming_connection.settimeout(SERVER_SOCKET_TIMEOUT)

    yield socket_for_incoming_connection, client_process

    client_process.kill()


def test_client_waiting_for_server(connected_client):
    """Client does not close right away if server has short delay."""
    socket_for_incoming_connection, client_process = connected_client
    time.sleep(PROCESS_SLEEP_TIME)
    assert client_process.exitcode is None, "Client does not wait for server and exited already."


def test_server_closed_connection_client_exited(connected_client):
    """Closing server before sending payload."""
    socket_for_incoming_connection, client_process = connected_client

    socket_for_incoming_connection.shutdown(SHUT_RDWR)
    socket_for_incoming_connection.close()
    time.sleep(PROCESS_SLEEP_TIME)

    assert client_process.exitcode is not None, "Client is still running even after server sent b"" closing message."


def test_server_closed_connection_client_exited_correctly(connected_client):
    """Closing server after sending payload, but not waiting for response."""
    socket_for_incoming_connection, client_process = connected_client
    data = token_bytes(SERVER_MESSAGE_LENGTH)
    socket_for_incoming_connection.sendall(data)

    socket_for_incoming_connection.shutdown(SHUT_RDWR)
    socket_for_incoming_connection.close()
    time.sleep(PROCESS_SLEEP_TIME)

    assert client_process.exitcode == 0, "Client exitcode indicates error."


def test_client_at_least_responded(connected_client, server_socket):
    """Client is at least capable of responding."""
    socket_for_incoming_connection, client_process = connected_client

    socket_for_incoming_connection.sendall(token_bytes(SERVER_MESSAGE_LENGTH))
    response = socket_for_incoming_connection.recv(32)

    assert response, "No response from client."


def test_client_responded_with_correct_hash(connected_client, server_socket):
    """Client correctly responds."""
    socket_for_incoming_connection, client_process = connected_client
    do_server_operation(socket_for_incoming_connection)


def test_client_server_conversation(connected_client, server_socket):
    """Client can operate for several iterations."""
    socket_for_incoming_connection, client_process = connected_client

    for _ in range(5):
        do_server_operation(socket_for_incoming_connection)