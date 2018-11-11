import random
from time import time

import sympy

from utils import jacobi_symbol


def fermat_primality(n, K=5):
    for i in range(K):
        a = random.randint(2, n - 2)
        if pow(a, (n - 1), n) != 1:
            return False
    return True


def solovay_strassen(n, K=10):
    if n == 2: return True
    if not n & 1: return False
    for k in range(K):
        a = random.randrange(2, n - 2)
        r = pow(a, (n - 1) // 2, n)
        if r != 1 and r != n - 1:
            return False
        s = jacobi_symbol(a, n) % n
        if r != s:
            return False
    return True


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


def test(n=3277, K=3):
    fermat = 0
    solo = 0
    milrab = 0
    for i in range(1000):
        if fermat_primality(n, K):
            fermat += 1
        if solovay_strassen(n, K):
            solo += 1
        if miller_rabin(n, K):
            milrab += 1
    print(fermat, solo, milrab)


def prime_error_test(f_test, n, K):
    err = 0
    g_res = sympy.isprime(n)
    for i in range(1000):
        if f_test(n, K) != g_res:
            err += 1
    return err


def speed_test(f_test, n, K, cnt):
    start = time()
    for i in range(cnt):
        f_test(n, K)
    return time() - start


def main():
    K = 1
    # test(3277, K)

    # test(1729, K)
    N = 1729
    # print(fermat_primality(N, K))
    # return
    # print(speed_test(fermat_primality, N, K, 200000))
    # print(speed_test(solovay_strassen, N, K, 200000))
    # print(speed_test(miller_rabin, N, K, 200000))

    trys = list(range(1, 6))
    for k in trys:
        print('Fermat err k={}: '.format(k), prime_error_test(fermat_primality, N, k))

    for k in trys:
        print('Solovey err k={}: '.format(k), prime_error_test(solovay_strassen, N, k))

    for k in trys:
        print('Miller err k={}: '.format(k), prime_error_test(miller_rabin, N, k))


if __name__ == '__main__':
    main()
