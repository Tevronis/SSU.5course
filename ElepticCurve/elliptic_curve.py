# -*- coding: utf-8 -*-
from random import randint

from utils import get_prime, complex_decomposition, inverse, legendre_symbol, isprime

INF = 100000


class EllipticPoint:
    def __init__(self, p, a=None, b=None):
        self.p = p
        self.x = randint(1, p) if a is None else a
        self.y = randint(1, p) if b is None else b

    @staticmethod
    def sum(P, Q, a, p):
        if EllipticPoint.iszero(P):
            return Q
        elif EllipticPoint.iszero(Q):
            return P
        if EllipticPoint.equal_inv(P, Q, p):
            return EllipticPoint(p, -1, -1)
        if not EllipticPoint.equal(P, Q):
            m = ((P.y - Q.y) % p) * inverse((P.x - Q.x) % p, p) % p
        else:
            m = (3 * P.x * P.x + a) * inverse((2 * P.y) % p, p) % p
        r = EllipticPoint(p)
        r.x = (m * m - P.x - Q.x) % p
        r.y = (-P.y + m * (P.x - r.x)) % p
        return r

    @staticmethod
    def mul(P, k, a, p):
        p_n = EllipticPoint(p, P.x, P.y)
        p_q = EllipticPoint(p, -1, -1)

        kbin = bin(k)[2:]
        m = len(kbin)
        for i in range(m):
            if kbin[m - i - 1] == '1':
                p_q = EllipticPoint.sum(p_q, p_n, a, p)

            p_n = EllipticPoint.sum(p_n, p_n, a, p)
        return p_q

    @staticmethod
    def equal(p, q):
        return p.x == q.x and p.y == q.y

    @staticmethod
    def equal_inv(p, q, mod):
        return p.x == q.x and p.y == -q.y % mod

    @staticmethod
    def iszero(p):
        return p.x == -1 and p.y == -1

    def __eq__(self, other):
        return EllipticPoint.equal(self, other)

    def __repr__(self):
        return self.x, self.y

    def __str__(self):
        return str([self.x, self.y])

    def __hash__(self):
        return (self.x * 31 + self.y) % self.p


def generator_elliptic_curve(l, m):
    while True:
        while True:
            p = get_prime(l)
            if p % 4 == 1:
                break

        a, b = complex_decomposition(1, p)
        assert a * a + b * b == p
        T = [-2 * a, -2 * b, 2 * a, 2 * b]
        for t in T:
            N = p + 1 + t
            if isprime(N // 2):
                r = N // 2
                break
            if isprime(N // 4):
                r = N // 4
                break
        else:
            continue

        good = True
        for i in range(1, m):
            if (p ** i) % r == 1:
                good = False
        if p == r or not good:
            continue

        while True:
            e = EllipticPoint(p)
            A = ((e.y ** 2 - e.x ** 3) * inverse(e.x, p)) % p
            good = False
            if N == r * 2:
                if legendre_symbol(-A, p) == -1:
                    good = True
            if N == r * 4:
                if legendre_symbol(-A, p) == 1:
                    good = True
            if not good:
                continue

            m = EllipticPoint.mul(e, N, A, p)
            if m == EllipticPoint(p, -1, -1):
                break
        Q = EllipticPoint.mul(e, N // r, A, p)
        return p, A, Q, r


def test():
    # p = EllipticPoint(17, 0)
    q = EllipticPoint(96, 26)
    N = 2 * 32413
    # aa = 3
    p = 97
    a = 2
    P = EllipticPoint(1, 10)
    print(EllipticPoint.mul(P, 2, a, p))
    # print(EllipticPoint.sum(p, q, a, f))


if __name__ == '__main__':
    test()
