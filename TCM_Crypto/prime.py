import random
from math import gcd

from utils import jacobi_symbol


def fermat_primality(n):
    bad = False
    for a in range(1, n):
        if gcd(a, n) == 1:
            if not (a ** (n - 1)) % n == 1:
                bad = True
                break
    return not bad


def solovay_strassen(num, K=10):
    if num == 2: return True
    if not num & 1: return False
    for k in range(1, K):
        a = random.randrange(1, num)
        if not gcd(a, num) > 1:
            b = a ** ((num - 1) // 2)
            r = jacobi_symbol(a, num)
            if (b - r) % num != 0:
                break
        else:
            break
    else:
        return True
    return False


def miller_rabin(n, K=10):
    if n == 2 or n == 3:
        return True

    if n < 2 or n % 2 == 0:
        return False

    s, t = 0, n - 1
    while t % 2 == 0:
        t //= 2
        s += 1

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


def main():
    for i in range(2, 1000):
        if not(fermat_primality(i) == miller_rabin(i) == solovay_strassen(i)):
            print(i, fermat_primality(i), miller_rabin(i), solovay_strassen(i))
            break


if __name__ == '__main__':
    main()
