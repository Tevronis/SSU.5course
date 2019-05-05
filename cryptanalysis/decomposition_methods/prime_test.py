import random


def miller_rabin(n, K=10):
    def getST(t):
        s = 0
        while t % 2 == 0:
                t //= 2
                s += 1
        return s, t

    if n == 2 or n == 3:
        return True

    if n < 2 or n % 2 == 0:
        return False

    s, t = getST(n - 1)
    for k in range(K):
        a = random.randrange(2, n - 2)
        x = pow(a, t, n)
        if x == 1 or x == n - 1:
            continue
        for i in range(1, s):
            x = (x * x) % n
            if x == 1:
                return False
            if x == n - 1:
                break
        if x != n - 1:
            return False
    return True