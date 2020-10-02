import os
import pickle
import socket
import asyncore
from typing import Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from custom_crypto import rsa
from sinks import DecryptSink, EncryptSink


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
        5. As soon as an application connects, the server starts reading data
           from the new socket, encrypts it and forwards it to the server
           (and vice versa)
    """

    def __init__(
        self,
        enc_addr: str,
        enc_port: int,
        app_addr: str,
        app_port: int
    ):

        super().__init__()
        self.__app_addr = app_addr
        self.__app_port = app_port

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

        print("[*] Encrypted session key sent, starting app server")

        app_sock = socket.create_server((self.__app_addr, self.__app_port))
        app_sock.listen(1)
        app, (app_ip, app_port) = app_sock.accept()

        print(f"[*] An app connected from {app_ip}:{app_port}, starting "
              "communication")

        srv_sink = DecryptSink(srv_sock, key)
        app_sink = EncryptSink(app, key)

        srv_sink.set_other(app_sink)
        app_sink.set_other(srv_sink)


if __name__ == "__main__":
    client = ProxyClient('127.0.0.1', 3333, "127.0.0.1", 4444)

    asyncore.loop()
