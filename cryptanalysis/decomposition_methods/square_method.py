from math import sqrt, gcd


def ferma(n, k, l, start):
    p = -1
    for i in range(start, l):
        s = int(sqrt(k*n)) + i
        # print(s)
        t = int(sqrt(pow(s, 2) - k*n))
        if t*t == pow(s, 2) - k*n:
            # print(t)
            p = gcd(k*n, s-t)
            p = gcd(p, n)
    return p


