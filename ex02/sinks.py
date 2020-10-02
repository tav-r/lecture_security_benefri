"""
The Sinks used by the ProxyServer and the ProxyClient to transfer the
data between the application and the encryption tunnel
"""

import asyncore
import os
import pickle
from typing import Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Sink(asyncore.dispatcher):
    """
    On each side of the encrypted tunnel, there are two sinks: one wraps
    the the socket which is connected to the other end of the tunnel and
    the other listens for a client application to connect.
    """

    def __init__(self, this):
        self.__other: Optional[Sink] = None
        self.__buf = b""
        asyncore.dispatcher.__init__(self, this)

    def set_other(self, other):
        """
        Set the other sink.

        This method should be called before the sink gets used because
        the sink writes data it receives into the buffer of the other
        sink.

        Args:
            other (Sink): the other sink
        """
        self.__other = other

    def readable(self):
        return not self.__buf and self.__other

    def handle_read(self):
        assert self.__other

        self.__other.buf += self.recv(4096*4)

    def handle_write(self):
        sent = self.send(self.__buf)
        self.__buf = self.__buf[sent:]

    def handle_close(self):
        self.close()
        if self.__other.other:
            self.__other.close()
            self.__other = None

    @property
    def other(self):
        """
        The other Sink (where received data is written to)
        """
        return self.__other

    @property
    def buf(self):
        """
        The buffer where the other sink stores the data before this sink sends
        them to its socket.
        """

        return self.__buf

    @buf.setter
    def buf(self, new_buf):
        self.__buf = new_buf


class EncryptSink(Sink):
    """
    A sink that encrypts received data before it writes it to the buffer of
    the other sink
    """
    def __init__(self, this, key):
        self.__key = key
        super().__init__(this)

    def handle_read(self):
        assert self.other

        aesgcm = AESGCM(self.__key)
        nonce = os.urandom(12)
        data = self.recv(4096*4)
        aad = b"???"
        cipher_text = aesgcm.encrypt(nonce, data, aad)
        self.other.buf += pickle.dumps((nonce, cipher_text, aad))


class DecryptSink(Sink):
    """
    A sink that decrypts received data before it writes it to the buffer of
    the other sink
    """
    def __init__(self, this, key):
        self.__key = key
        super().__init__(this)

    def handle_read(self):
        assert self.other

        nonce, cipher_text, aad = pickle.loads(self.recv(4096*4))
        aesgcm = AESGCM(self.__key)
        self.other.buf += aesgcm.decrypt(nonce, cipher_text, aad)
