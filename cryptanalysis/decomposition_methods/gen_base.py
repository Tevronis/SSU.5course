from math import sqrt, exp, log

import prime_test


def make_base(l):
    base = [2, 3, 5]
    tmp = 7
    while len(base) != l:
        if prime_test.miller_rabin(tmp):
            base.append(tmp)
        tmp += 1
    return base


def legendre_symbol(B, p, d=2):
    if B % p == 0:
        return 0
    if B == 1:
        return 1
    res = pow(B, (p - 1) // d, p)
    if res != 1:
        res = -1
    return res


def make_base_dixon(n):
    base = [2, 3, 5]
    p = int(sqrt(exp(sqrt(log(n)*log(log(n))))))
    tmp = 7
    while tmp <= p:
        if prime_test.miller_rabin(tmp):
            base.append(tmp)
        tmp += 1
    base = [-1] + list(filter(lambda x: legendre_symbol(n, x) == 1, base))
    return base

