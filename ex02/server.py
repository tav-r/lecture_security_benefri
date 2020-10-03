"""
Implementation of the proxy server.
"""
import asyncore
import pickle
import socket

from typing import Tuple
from subprocess import check_output

from custom_crypto import rsa
from sinks import EncryptSink, DecryptSink


def print_usage(prog_name):
    """Print program usage"""
    print(f"Usage: {prog_name} LISTEN_ADDRESS LISTEN_PORT CONNECTION_ADDRESS "
          f"CONNECTION_PORT")


def get_rsa_keys(keysize: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Get a hardcorded rsa pub/private key pair.
    """

    p = int(
        check_output(
            ["openssl", "prime", "-generate", "-bits", str(keysize // 2)]
        ).decode().strip())
    q = int(
        check_output(
            ["openssl", "prime", "-generate", "-bits", str(keysize // 2)]
        ).decode().strip())

    return rsa.gen_key(p, q, 2**16+1)


class ProxyServer(asyncore.dispatcher):
    """
    A proxy server for an encrypted tunnel.

    The "protocol" works like this:
        1. When the proxy client connects, an rsa public key is sent
        2. The server waits for the client to send an encrypted AES-GCM key
        3. The server connects to the given application port
        4. When successfully connected, the server starts...:
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
        app_port: int,
        rsa_keysize=2048
    ):
        super().__init__()

        self.__app_addr = app_addr
        self.__app_port = app_port
        self.__key = None

        print(f"[*] Generating key pair (keysize = {rsa_keysize})")

        self.__pub_key, self.__priv_key = get_rsa_keys(rsa_keysize)

        # start listening for incoming connection from the client
        self.create_socket()
        self.set_reuse_addr()
        self.bind((enc_addr, enc_port))
        self.listen(1)

        print(f"[*] Encryption server started, listening for connections at "
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

        app = socket.create_connection((self.__app_addr, self.__app_port))

        print(f"[*] An app connected from {app_ip}:{app_port}, starting "
              f"communication")

        srv_sink = DecryptSink(sock, self.__key)
        app_sink = EncryptSink(app, self.__key)

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
        one = ProxyServer(srv_ip, int(srv_port), app_ip, int(app_port))
    except ValueError:
        print("Invalid port number")
        sys_exit(EX_USAGE)

    asyncore.loop()
