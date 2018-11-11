import random
import hashlib

from elliptic_curve import generator_elliptic_curve, EllipticPoint as ep
from utils import inverse

hashf = hashlib.sha256


def key_generation(G, a, p):
    k = random.randint(1, p - 1) # private key
    A = ep.mul(G, k, a, p)


def hsh(m, p):
    return int.from_bytes(hashf(m).digest(), byteorder='big') % p


def signature(M, G, a, p, x):
    r, k, R = 0, None, None
    while r == 0:
        k = random.randint(1, p - 1)
        R = ep.mul(G, k, a, p)
        r = R.x % p

    e = hsh(M, p)
    s = (e + ep.mul(R, x, a, p)) * inverse(k, r) % r
    return R, s


def verify(M, R, s, a, p):
    assert 1 <= s <= p
    A = read_param('Alice public key')
    G = read_param('generated point')
    # R in EC
    V1 = ep.mul(R, s, a, p)
    V2 = ep.sum(ep.mul(G, hsh(M, p), a, p), ep.mul(A, R.x, a, p), a, p)
    return V1 == V2


def main():
    pass
    # 3



if __name__ == '__main__':
    main()