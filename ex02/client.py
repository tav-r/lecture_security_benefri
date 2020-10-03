import os
import pickle
import socket
import asyncore
from typing import Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from custom_crypto import rsa
from sinks import DecryptSink, EncryptSink


def print_usage(prog_name):
    """Print program usage"""
    print(f"Usage: {prog_name} CONNECTION_ADDRESS CONNECTION_PORT "
          f"PROXY_ADDRESS PROXY_PORT")


class ProxyClient(asyncore.dispatcher):
    """
    A proxy client for an encrypted tunnel.

    The "protocol" works like this:
        1. The client tries to connect to the proxy server
        2. When a connection was established, the client reads a public rsa
           key from the new socket
        3. The client generates a symmetric AES-GCM session key and sends it
           to the server
        4. The client starts listening for an application to connect
        5. When an application is connected, the server starts...:
            a) ...reading data from the application, encrypts it and forwards
               it to the client
            b) ...reading data from the client, decrypts it and forwards it to
               the application
    """
 
    def __init__(
        self,
        enc_addr: str,
        enc_port: int,
        app_addr: str,
        app_port: int
    ):

        super().__init__()

        print("[*] Connecting to server")

        srv_sock: socket.socket = socket.create_connection(
            (enc_addr, enc_port)
        )

        print(f"[*] Connection to {enc_addr}:{enc_port} established")

        pub_key: Tuple[int, int] = pickle.loads(srv_sock.recv(2048))

        print("[*] Received public key from server, generating"
              "symmetric session key")

        key: bytes = AESGCM.generate_key(bit_length=128)
        cipher: bytes = rsa.encrypt(key, pub_key)

        srv_sock.send(cipher)

        print(f"[*] Encrypted session key sent, starting app server at "
              f"{app_addr}:{app_port}")

        app_sock = socket.create_server((app_addr, app_port))
        app_sock.listen(5)
        app, (app_ip, app_port) = app_sock.accept()

        print(f"[*] An app connected from {app_ip}:{app_port}, starting "
              f"communication")

        srv_sink = DecryptSink(srv_sock, key)
        app_sink = EncryptSink(app, key)

        srv_sink.set_other(app_sink)
        app_sink.set_other(srv_sink)


if __name__ == "__main__":
    from sys import argv, exit as sys_exit
    from os import EX_USAGE

    if len(argv) != 5:
        print_usage(argv[0])
        sys_exit(EX_USAGE)

    _, srv_ip, srv_port, app_ip, app_port = argv

    try:
        one = ProxyClient(srv_ip, int(srv_port), app_ip, int(app_port))
    except ValueError:
        print("Invalid port number")
        sys_exit(EX_USAGE)

    asyncore.loop()
