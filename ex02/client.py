import os
import pickle
import socket
import asyncore
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from custom_crypto import rsa
from sinks import DecryptSink, EncryptSink


class ProxyClient(asyncore.dispatcher):
    def __init__(
        self,
        enc_addr: str,
        enc_port: int,
        app_addr: str,
        app_port: int
    ):

        self.__app_addr = app_addr
        self.__app_port = app_port

        srv_sock = socket.create_connection((enc_addr, enc_port))

        pub_key = pickle.loads(srv_sock.recv(2048))

        key = AESGCM.generate_key(bit_length=128)
        cipher = rsa.encrypt(pickle.dumps(key), pub_key)

        srv_sock.send(cipher)

        app_sock = socket.create_server((self.__app_addr, self.__app_port))
        app_sock.listen(1)
        app, _ = app_sock.accept()

        srv_sink = DecryptSink(srv_sock, key)
        app_sink = EncryptSink(app, key)

        srv_sink.set_other(app_sink)
        app_sink.set_other(srv_sink)


if __name__ == "__main__":
    client = ProxyClient('127.0.0.1', 3333, "127.0.0.1", 4444)

    asyncore.loop()
