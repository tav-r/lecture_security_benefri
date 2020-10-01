from typing import List, Optional, Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import asyncore
import socket
import pickle
import logging

from custom_crypto import rsa
from sinks import EncryptSink, DecryptSink


def get_default_rsa_keys() -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Get a hardcorded rsa pub/private key pair.
    """

    p = 287756783560809232147319204051814079727
    q = 301571122384786708958989910930476973377
    return rsa.gen_key(p, q, 2**16+1)


class ProxyServer(asyncore.dispatcher):
    def __init__(
        self,
        enc_addr: str,
        enc_port: int,
        app_addr: str,
        app_port: int
    ):
        asyncore.dispatcher.__init__(self)

        self.__app_addr = app_addr
        self.__app_port = app_port
        self.__key = None

        print("[*] Generating key pair")

        self.__pub_key, self.__priv_key = get_default_rsa_keys()

        self.create_socket()
        self.set_reuse_addr()
        self.bind((enc_addr, enc_port))
        self.listen(5)

        print("[*] Encryption server started")

    def handle_accepted(self, conn, addr):
        ip, port = addr
        print("[*] New connection from {ip}:{port}, sending pub_key")

        # initailly send pub_key
        ser_pub_key = pickle.dumps(self.__pub_key)
        while ser_pub_key:
            sent = conn.send(ser_pub_key)
            ser_pub_key = ser_pub_key[sent:]

        print("[*] Waiting for symmetric key")

        sym_key_enc = conn.recv(2048)
        self.__key = pickle.loads(rsa.decrypt(sym_key_enc, self.__priv_key))

        print("[*] Got symmetric key, starting app server")

        app_sock = socket.create_server((self.__app_addr, self.__app_port))
        app_sock.listen(1)
        app, _ = app_sock.accept()

        srv_sink = DecryptSink(conn, self.__key)
        app_sink = EncryptSink(app, self.__key)

        srv_sink.set_other(app_sink)
        app_sink.set_other(srv_sink)


if __name__ == "__main__":
    one = ProxyServer('127.0.0.1', 3333, '127.0.0.1', 3000)

    asyncore.loop() 
