# from contextlib import suppress
from hashlib import sha256
from socket import AF_INET, SOCK_STREAM, socket
from typing import Tuple


def socket_client(address: Tuple[str, int], server_message_length: int):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(address)
        while True:
            try:
                data = sock.recv(server_message_length)
                if not data:
                    break
                resp = sha256(data).digest()
                sock.sendall(resp)
            except IOError:
                return
