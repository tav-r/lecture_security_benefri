"""
A custom implementation of schoolbook RSA.

Tests can be run calling python with the '-v' flag, like
`pyhton rsa.py -v`
"""

from typing import Tuple, Iterator
from random import randint


def rand_coprime(num: int) -> int:
    """
    Brute force a number that is coprime to the given number.

    Args:
        n (int): number that the result should be coprime to

    Returns:
        int: a number coprime to the given number

    Examples:
        >>> n = 34232
        >>> r, _, _ = lin_combi(rand_coprime(n), n)
        >>> r == 1
        True
    """

    rand_cop = randint(2, num - 1)
    while not lin_combi(num, rand_cop)[0] == 1:
        rand_cop = randint(2, num - 1)

    return rand_cop



def lin_combi(a: int, b: int):
    """
    Calculate (c, d) such that a * c + b * d = gcd(a, b)

    Args:
        a (int): the number the multiplicative inverse should
                 be calculated for
        n (int): ...
    Returns:
        Tuple[int, int]: ...

    Examples:
        >>> lin_combi(99, 78)
        (3, -11, 14)
        >>> lin_combi(78, 99)
        (3, 14, -11)
    """

    if not b:
        return (a, 1, 0)

    d, x, y = lin_combi(b, a % b)
    
    return d, y, x - (a // b) * y
    

def gen_key(p: int,
            q: int, 
            e: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Args:
        p (int): ...
        q (int): ...
        e (int): ...

    Returns:
        Tuple[Tuple[int, int], Tuple[int, int]]: ...

    Examples:
        >>> gen_key(11, 13, 23)
        ((23, 143), (47, 143))
        >>> pub_key, priv_key = gen_key(11, 13, 23)
        >>> decrypt(encrypt(b"\x07", pub_key), priv_key) == b"\x07"
        True
        >>> p = 287756783560809232147319204051814079727
        >>> q = 301571122384786708958989910930476973377
        >>> pub_key, priv_key = gen_key(p, q, 2**16+1)
        >>> c = encrypt(b"Hello world", pub_key)
        >>> decrypt(c, priv_key) == b"Hello world"
        True
    """

    assert p > 0
    assert q > 0
    assert q > 0
    # I would have to import sympy for these assert statements to work
    # assert isprime(p)
    # assert isprime(q)

    N = p * q
    phi_N = (p - 1) * (q - 1)

    one, d, k = lin_combi(e, phi_N)
    
    assert one == 1
    assert d * e + k * phi_N == 1

    # map negative results back into ring of integers module phi_N
    d = phi_N + d if d < 0 else d

    return (e, N), (d, N)


def bytes_to_int(bytestr: bytes) -> int:
    """
    Convert a byte string into a number

    Args:
        bytes: byte string representing to convert

    Returns:
        number (int): number from byte string

    Examples:
        >>> bytes_to_int(b"DCBA") == 0x44434241
        True
        >>> bytes_to_int(b"\x07") == 7
        True
    """

    return sum(
        [b << (i*8) for (b, i) in
         zip(bytestr, range(len(bytestr) - 1, -1, -1))]
    )


def int_to_bytes(number: int) -> bytes:
    """
    Convert an integer to a byte string

    Args:
        number (int): number to convert

    Returns:
        bytes: byte string representing the given number

    Examples:
        >>> int_to_bytes(0x41424344)
        b'ABCD'
        >>> int_to_bytes(7) == b"\x07"
        True
    """
    def _int_to_bytes() -> Iterator[int]:
        n = number

        while n:
            r = n & 0xff
            n >>= 8
            yield r

    return bytes(reversed(list(_int_to_bytes())))


def encrypt(m: bytes, pub_key: Tuple[int, int]) -> bytes:
    """
    Examples:
        >>> encrypt(b"\x07", (23, 143)) == b"\x02"
        True
    """
    e, n = pub_key
    return int_to_bytes((bytes_to_int(m) ** e) % n)

def decrypt(m: bytes, priv_key: Tuple[int, int]) -> bytes:
    """
    Examples:
        >>> decrypt(b"\x02", (47, 143)) == b"\x07"
        True
    """

    d, n = priv_key
    return int_to_bytes(pow(bytes_to_int(m), d, n))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
