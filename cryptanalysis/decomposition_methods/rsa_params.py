import random
from math import gcd

import prime_test


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


def gen_params():
    p_len = int(input('Длина p (биты): '))
    q_len = int(input('Длина q (биты): '))
    p = random.randint(2 ** (p_len - 1), 2 ** p_len)
    q = random.randint(2 ** (q_len - 1), 2 ** q_len)
    while not prime_test.miller_rabin(p):
        p = random.randint(2 ** (p_len - 1), 2 ** p_len)
    while not prime_test.miller_rabin(q) or p == q:
        q = random.randint(2 ** (q_len - 1), 2 ** q_len)
    with open('pq.txt', 'w') as fout_pq:
        fout_pq.write(str(p) + ' ' + str(q))

    n = p*q
    phi = (p-1)*(q-1)

    while True:
        e = random.randint(10, phi-1)
        if gcd(e, phi) == 1:
            break
    with open('pub_key.txt', 'w') as fout_public:
        fout_public.write(str(n) + ' ' + str(e))

    with open('n_phi.txt', 'w') as fout_n:
        fout_n.write(str(n) + ' ' + str(phi))

    d = inverse(e, phi)
    with open('sec_key.txt', 'w') as fout_secret:
        fout_secret.write(str(d))
    print('Сохранен файл pub_key.txt')
    print('Сохранен файл n_phi.txt')
    print('Сохранен файл sec_key.txt')
