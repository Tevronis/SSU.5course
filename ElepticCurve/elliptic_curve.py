from random import randint

from utils import inverse

INF = 100000


class EllipticPoint:
    def __init__(self, a=None, b=None, p=INF):
        if a is None and b is None:
            self.x = randint(1, p)
            self.y = randint(1, p)
        else:
            self.x = a
            self.y = b

    @staticmethod
    def rand_point(p):
        return EllipticPoint(None, None, p)

    @staticmethod
    def sum(P, Q, a, p):
        if EllipticPoint.iszero(P):
            return Q
        elif EllipticPoint.iszero(Q):
            return P
        if EllipticPoint.equal_inv(P, Q, p):
            return EllipticPoint(0, 0)
        if not EllipticPoint.equal(P, Q):
            m = ((P.y - Q.y) % p) * inverse((P.x - Q.x) % p, p) % p
        else:
            m = (3 * P.x * P.x + a) * inverse((2 * P.y) % p, p) % p
        r = EllipticPoint()
        r.x = (m * m - P.x - Q.x) % p
        r.y = (-P.y + m * (P.x - r.x)) % p
        #r.y = (Q.y + m * (r.x - Q.x)) % p
        return r

    @staticmethod
    def mul(p, k, a, mod):
        p_n = EllipticPoint(p.x, p.y)
        p_q = EllipticPoint(0, 0)

        kbin = bin(k)[2:]
        m = len(kbin)
        for i in range(m):
            if kbin[m - i - 1] == '1':
                p_q = EllipticPoint.sum(p_q, p_n, a, mod)
            p_n = EllipticPoint.sum(p_n, p_n, a, mod)
        return p_q

    @staticmethod
    def equal(p, q):
        return p.x == q.x and p.y == q.y

    @staticmethod
    def equal_inv(p, q, mod):
        return p.x == q.x and p.y != q.y and pow(p.y, 2, mod) == pow(q.y, 2, mod)

    @staticmethod
    def iszero(p):
        return p.x == 0 and p.y == 0

    @staticmethod
    def getinf():
        return EllipticPoint(0, 0)

    def __eq__(self, other):
        return EllipticPoint.equal(self, other)

    def __repr__(self):
        return self.x, self.y

    def __str__(self):
        return str([self.x, self.y])


if __name__ == '__main__':
    #p = EllipticPoint(17, 0)
    q = EllipticPoint(96, 26)
    N = 2 * 32413
    #aa = 3
    f = 97
    a = 2
    p = EllipticPoint(1, 10)
    print(EllipticPoint.mul(p, 2, a, f))
    #print(EllipticPoint.sum(p, q, a, f))
