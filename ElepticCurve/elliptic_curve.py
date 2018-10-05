# -*- coding: utf-8 -*-
from random import randint

from utils import inverse

INF = 100000


class EllipticPoint:
    def __init__(self, p, a=None, b=None):
        if a is None or b is None:
            self.x = randint(1, p)
            self.y = randint(1, p)
        else:
            self.x = a
            self.y = b

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
        return p.x == q.x and p.y != q.y and pow(p.y, 2, mod) == pow(q.y, 2, mod)

    @staticmethod
    def iszero(p):
        return p.x == -1 and p.y == -1

    def __eq__(self, other):
        return EllipticPoint.equal(self, other)

    def __repr__(self):
        return self.x, self.y

    def __str__(self):
        return str([self.x, self.y])


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
