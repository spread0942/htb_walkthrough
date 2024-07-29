from rsa import lcm, get_d, PrivateKey


def factor(n):
    for p in range(2, n):
        if n % p == 0:
            return p, n//p

def decrypt(pub, c):
    p, q = factor(pub.n)
    lambda_n = lcm(p-1, q-1)
    d = get_d(pub.e, lambda_n)
    priv = PrivateKey(d, pub.n)
    return priv.decrypt_message(c)