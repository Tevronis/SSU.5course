import random
from math import gcd, log


def method(n, base):
    # print(base)
    a = random.randint(2, n-2)
    d = gcd(a, n)
    if d >= 2:
        return d
    for item in base:
        l = int(log(n) / log(item))
        a = pow(a, pow(item, l), n)
    d = gcd(a-1, n)
    if d == 1 or d == n:
        d = -1
        return d
    else:
        return d


