# -*- coding: utf-8 -*-
import sys

from elliptic_curve import EllipticPoint

from utils import get_prime, complex_decomposition, inverse, legendre_symbol, isprime


def generator_elliptic_curve(l, m, prt=False):
    while True:
        if prt: print('Step 1.')
        while True:
            p = get_prime(l)
            if p % 4 == 1:
                break

        if prt: print('Step 2.')
        a, b = complex_decomposition(1, p)
        assert a * a + b * b == p
        if prt: print('Step 3.')
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

        if prt: print('Step 4.')
        good = True
        for i in range(1, m):
            if (p ** i) % r == 1:
                good = False
        if p == r or not good:
            continue

        if prt: print('Step 5.')
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

            if prt: print('Step 6.')
            m = EllipticPoint.mul(e, N, A, p)
            if m == EllipticPoint(p, 0, 0):
                break
            if prt: print('Step 7.')
        Q = EllipticPoint.mul(e, N // r, A, p)
        if prt: print('Step 8.')
        return p, A, Q, r


def plot(values):
    import matplotlib.pyplot as plt
    X = [item[0] for item in values]
    Y = [item[1] for item in values]

    plt.scatter(X, Y, s=1)
    plt.show()


def main(args):
    if len(args) == 1:
        l, m = 50, 72
    else:
        l, m = map(int, args[1:])

    p, A, Q, r = generator_elliptic_curve(l, m)
    dots = [Q]
    print("p: {}, A: {}, Q: {}, r: {}".format(p, A, Q.__repr__(), r))
    print('Q * r:', EllipticPoint.mul(Q, r, A, p))
    for i in range(10000):
        pp = EllipticPoint.sum(Q, dots[i], A, p)
        dots.append(pp)
    dots = [[item.x, item.y] for item in dots]
    plot(dots)


if __name__ == '__main__':
    main(sys.argv)
