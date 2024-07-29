import math
import random


def is_prime(p):
    for i in range(2, math.isqrt(p)):
        if p % i == 0:
            return False
    return True


def get_prime(size):
    while True:
        p = random.randrange(size, 2*size)
        if is_prime(p):
            return p


def lcm(a, b):
    return a*b//math.gcd(a, b)


def get_e(lambda_n):
    for e in range(2, lambda_n):
        if math.gcd(e, lambda_n) == 1:
            return e
    return False


def get_d(e, lambda_n):
    for d in range(2, lambda_n):
        if d*e % lambda_n == 1:
            return d
    return False


def key_generation(size):
    # Step 1:
    p = get_prime(size)
    q = get_prime(size)

    # Step 2
    n = p*q

    # Step 3:
    lambda_n = lcm(p-1, q-1)

    # Step 4:
    e = get_e(lambda_n)

    # Step 5:
    d = get_d(e, lambda_n)
    
    priv = PrivateKey(d, n)
    pub = PublicKey(e, n)
    
    return (priv, pub)


class PublicKey:
    def __init__(self, e, n) -> None:
        self.e = e
        self.n = n
    
    def encrypt_message(self, m):
        return m**self.e % self.n

class PrivateKey:
    def __init__(self, d, n) -> None:
        self.d = d
        self.n = n
    
    def decrypt_message(self, c):
        return c**self.d % self.n
