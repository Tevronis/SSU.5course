import json
import random

import sympy


def get_big_digit(a=10 ** 100, b=10 ** 110):
    return random.randint(a, b)


def get_big_prime(a=10 ** 100, b=10 ** 110):
    return sympy.randprime(a, b)


def read_param(file, param):
    with open(file) as f:
        ff = json.load(f)
    return ff[param]


def save_param(file, paramname, param):
    with open(file, 'w') as f:
        json.dump({paramname: param}, f)


def write_log(line, file='log.log'):
    with open(file, 'a') as f:
        f.write(line + '\n')


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
    # pg = 2
    # while True:
    #     if pow(g, p, p) == 1:
    #         break
    #     g += 1
    # return g
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


def extended_euclid(a, b):
    if b == 0:
        d = a
        x = 1
        y = 0
        return x, y, d

    x2 = 1
    x1 = 0
    y2 = 0
    y1 = 1
    while b > 0:
        q = a // b
        r = a - q * b
        x = x2 - q * x1
        y = y2 - q * y1
        a = b
        b = r
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y
    d = a
    x = x2
    y = y2
    return x, y, d


def inverse(a, n):
    x, y, d = extended_euclid(a, n)
    if d == 1:
        x = (x % n + n) % n
        return x
    return 0


if __name__ == '__main__':
    n = int(input("Generator tst: "))

    print('Первообразный корень по модулю {}: '.format(n) + str(generator(n)))
