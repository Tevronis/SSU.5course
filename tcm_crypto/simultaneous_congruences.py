import functools
import sys
from operator import mul

import utils


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


def main(argv):
    """
    sample:
    a: 2 1 3 8
    m: 5 7 11 13
    """
    mod = argv[2]
    a = [int(item) for item in input('a: ').split()]
    m = [int(item) for item in input('m: ').split()]
    #if mod == 1:
    print(chinese_theorem(a, m))
    #if mod == 2:
    print(garner(a, m))


if __name__ == '__main__':
    main(sys.argv)
