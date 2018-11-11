import random

import sympy

from euclid import euclid_extended


MAX_B_SIZE = 5000
MAX_SUBSET = 30


def get_big_digit(a=10 ** 100, b=10 ** 110):
    return random.randint(a, b)


def get_big_prime(a=10 ** 100, b=10 ** 110):
    return sympy.randprime(a, b)


def jacobi_symbol(m, n):
    return sympy.jacobi_symbol(m, n)


def phi(n):
    result = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n /= i
            result -= result // i
        i += 1
    if n > 1:
        result -= result / n
    return result


def generator(p):
    ph = p - 1
    n = ph
    fact = []
    for k, v in sympy.factorint(n).items():
        fact.extend([k] * v)

    for res in range(2, p):
        ok = True
        for i in range(0, len(fact)):
            if not ok:
                break
            ok &= pow(res, ph // fact[i], p) != 1
        if ok:
            return res

    return -1


def inverse(a, n):
    x, y, d = euclid_extended(a, n)
    if d == 1:
        x = (x % n + n) % n
        return x
    return 0


def generate_base(desired_count):
    base = [2, 3, 5]
    counter = 7
    while len(base) < desired_count:
        for b in base:
            if counter % b == 0:
                break
            if b > counter // 2:
                base.append(counter)
                break
        counter += 1
    return base


def legendre(a, n):
    a %= n
    if a == 0:
        return 0
    elif a == 1:
        return 1
    return pow(a, (n - 1) // 2, n)


def fac2k(a):
    k = 0
    while a & 1 == 0:
        a >>= 1
        k += 1
    return a, k


def test():
    n = int(input("Generator tst: "))

    print('Первообразный корень по модулю {}: '.format(n) + str(generator(n)))


if __name__ == '__main__':
    test()
