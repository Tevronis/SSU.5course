import functools
from operator import mul

import utils


def euclid(a, b):
    assert 0 < b <= a
    r = [a, b]
    i = 1
    while True:
        r.append(r[i - 1] % r[i])
        if r[i + 1] == 0:
            d = r[i]
            break
        i += 1
    return d


def euclid_bin(a, b):
    assert 0 < b <= a
    g = 1
    while a % 2 == 0 and b % 2 == 0:
        a >>= 1
        b >>= 1
        g <<= 1
    u = a
    v = b
    while u != 0:
        while u % 2 == 0:
            u >>= 1
        while v % 2 == 0:
            v >>= 1
        if u >= v:
            u = u - v
        else:
            v = v - u
    d = g * v
    return d


def euclid_extended(a, b):
    assert 0 < b <= a
    r = [a, b]
    x = [1, 0]
    y = [0, 1]
    i = 1
    q = [0]
    while True:
        q.append(r[i - 1] // r[i])
        r.append(r[i - 1] % r[i])
        if r[i + 1] == 0:
            d = r[i]
            X = x[i]
            Y = y[i]
            break
        else:
            x.append(x[i - 1] - q[i] * x[i])
            y.append(y[i - 1] - q[i] * y[i])
            i += 1
    return d, X, Y


def chinese_theorem(a, e):
    m = functools.reduce(mul, e)
    u = 0
    for idx in range(len(a)):
        u += a[idx] * (m // e[idx]) * utils.inverse(m // e[idx], e[idx])
    return u % m


def garner(r, m):
    n = len(m)
    c = [0] * n
    for i in range(1, n):
        c[i] = 1
        for j in range(0, i):
            u = utils.inverse(m[j], m[i])
            c[i] = u * c[i] % m[i]
    u = r[0]
    x = u
    for i in range(1, n):
        u = (r[i] - x) * c[i] % m[i]
        x = x + u * functools.reduce(mul, (m[idx] for idx in range(i)), 1)
    return x


def main():
    """
    simple for Garner and Chine theorem
    a: 2 1 3 8
    m: 5 7 11 13
    """
    mod = int(input('1 - Chine theorem, 2 - Garner, 3 - Euclides '))
    if mod != 3:
        a = [int(item) for item in input('a: ').split()]
        m = [int(item) for item in input('m: ').split()]
        if mod == 1:
            print(chinese_theorem(a, m))
        if mod == 2:
            print(garner(a, m))
    else:
        a, b = list(map(int, input('a, b: ').split()))
        print('gcd: ', euclid(a, b))
        print('gcd binary: ', euclid_bin(a, b))
        print('gcd extended, x, y: ', euclid_extended(a, b))


if __name__ == '__main__':
    main()
