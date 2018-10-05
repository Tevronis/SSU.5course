# -*- coding: utf-8 -*-
import sys
from time import time

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
            if m == EllipticPoint(p, -1, -1):
                break
            if prt: print('Step 7.')
        Q = EllipticPoint.mul(e, N // r, A, p)
        if prt: print('Step 8.')
        return p, A, Q, r


def plot(values):
    import matplotlib.pyplot as plt
    X = [item[0] for item in values if item[0] != -1]
    Y = [item[1] for item in values if item[1] != -1]

    plt.scatter(X, Y, s=1)
    plt.show()


def main(args):
    if len(args) == 1:
        l, m = 10, 72
    else:
        l, m = map(int, args[1:])
    start = time()
    p, A, Q, r = generator_elliptic_curve(l, m)
    print('Time to gen:', time() - start)
    # p = 773
    # A, Q, r = 78, EllipticPoint(p, 117, 386), 408
    dots = [Q]
    print("p: {}, A: {}, Q: {}, r: {}".format(p, A, Q.__repr__(), r))
    print('Q * r:', EllipticPoint.mul(Q, r, A, p))
    if l < 20:
        for i in range(r - 1):
            pp = EllipticPoint.sum(Q, dots[i], A, p)
            dots.append(pp)
        dots = [[item.x, item.y] for item in dots]
        assert r == len(dots)
        open('dots.txt', 'w').write(''.join(list(map(str, dots))))
        plot(dots)


if __name__ == '__main__':
    main(sys.argv)
