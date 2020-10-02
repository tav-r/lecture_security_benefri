from typing import List, Optional, Tuple
import asyncore
import pickle
import socket

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
    """
    A proxy server for an encrypted tunnel.

    The "protocol" works like this:
        1. When the proxy client connects, an rsa public key is sent
        2. The server waits for the client to send an encrypted AES-GCM key
        3. The server starts listening for a connection from an application
        4. As soon as an application connects, the server starts reading data
           from the new socket, encrypts it and forwards it to the client
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
        self.__key = None

        print("[*] Generating key pair")

        self.__pub_key, self.__priv_key = get_default_rsa_keys()

        # start listening for incoming connection from the client
        self.create_socket()
        self.set_reuse_addr()
        self.bind((enc_addr, enc_port))
        self.listen(1)

        print(f"[*] Encryption server started, listening for connections at"
              f"{enc_addr}:{enc_port}")

    def handle_accepted(self, sock, addr):
        client_ip, client_port = addr
        print(f"[*] New connection from {client_ip}:{client_port}, "
              "sending pub_key")

        # initailly send pub_key
        ser_pub_key: bytes = pickle.dumps(self.__pub_key)
        while ser_pub_key:
            sent = sock.send(ser_pub_key)
            ser_pub_key = ser_pub_key[sent:]

        print("[*] Waiting for symmetric key")

        sym_key_enc = sock.recv(2048)
        self.__key = rsa.decrypt(sym_key_enc, self.__priv_key)

        print(f"[*] Encrypted tunnel established, starting app server at "
              f"{self.__app_addr}:{self.__app_port}")

        app_sock = socket.create_server((self.__app_addr, self.__app_port))
        app_sock.listen(5)
        app, (app_ip, app_port) = app_sock.accept()

        print(f"[*] An app connected from {app_ip}:{app_port}, starting "
              f"communication")

        srv_sink = DecryptSink(sock, self.__key)
        app_sink = EncryptSink(app, self.__key)

        srv_sink.set_other(app_sink)
        app_sink.set_other(srv_sink)


if __name__ == "__main__":
    one = ProxyServer('127.0.0.1', 3333, '127.0.0.1', 3000)

    asyncore.loop()
