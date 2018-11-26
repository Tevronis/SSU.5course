from random import randint

from utils import inverse


def gen_ellip_point(p, a=None, b=None):
    if a is None or b is None:
        return [randint(1, p), randint(1, p)]
    else:
        return [a, b]


def sum(P, Q, a, p):
    if iszero(P):
        return Q
    elif iszero(Q):
        return P
    if equal_inv(P, Q, p):
        return [-1, -1]
    if not equal(P, Q):
        m = ((P[1] - Q[1]) % p) * inverse((P[0] - Q[0]) % p, p) % p
    else:
        m = (3 * P[0] * P[0] + a) * inverse((2 * P[1]) % p, p) % p
    r = [0, 0]
    r[0] = (m * m - P[0] - Q[0]) % p
    r[1] = (-P[1] + m * (P[0] - r[0])) % p
    return r


def mul(P, k, a, p):
    p_n = [P[0], P[1]]
    p_q = [-1, -1]

    kbin = bin(k)[2:]
    m = len(kbin)
    for i in range(m):
        if kbin[m - i - 1] == '1':
            p_q = sum(p_q, p_n, a, p)

        p_n = sum(p_n, p_n, a, p)
    return p_q


def equal(p, q):
    return p[0] == q[0] and p[1] == q[1]


def equal_inv(p, q, mod):
    return p[0] == q[0] and p[1] == -q[1] % mod


def iszero(p):
    return p[0] == -1 and p[1] == -1


