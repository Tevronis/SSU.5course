import random
from math import gcd


def decomposition():
    with open('pub_key.txt', 'r') as fin:
        n, e = map(int, fin.read().split())
    with open('sec_key.txt', 'r') as fin:
        d = int(fin.read())

    f = 0
    while True:
        f += 1
        s = (e*d - 1) // 2**f
        if (e*d - 1) % 2**f == 0 and s % 2 == 1:
            break
    u = -1
    while u == -1:
        a = random.randint(2, n-2)
        u = pow(a, s, n)
        v = pow(u, 2, n)

        while v != 1:
            u = v
            v = pow(u, 2, n)

    p = gcd(u-1, n)
    q = gcd(u+1, n)

    return p, q






