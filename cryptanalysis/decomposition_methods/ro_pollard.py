from math import gcd


def f(x, n, p, s):
    x = (pow(x, p) + s) % n
    return x


def method(n, c, p=2, s=2):
    a = c
    b = c
    d = 1
    while d == 1:
        a = f(a, n, p, s)
        b = f(f(b, n, p, s), n, p, s)
        d = gcd(a-b, n)
    if d == n:
        ans = -1
    else:
        ans = d
    return ans


