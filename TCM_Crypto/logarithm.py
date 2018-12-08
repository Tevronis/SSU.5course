import math
import random
import sys
import time

import sympy

import euclid
import factorization
import utils


def factorize(n):
    base = {}
    n, k = utils.fac2k(n)
    if k > 0:
        base[2] = k
    while n > 1:
        divisor = factorization.ppollard(n) if not sympy.isprime(n) else n
        if divisor is None:
            raise ValueError('Ошибка при факторизации')
        if divisor not in base:
            base[divisor] = 0
        base[divisor] += 1
        n //= divisor
    return base


def primitive_root(p, count=1):
    """Только для простых p"""
    assert sympy.isprime(p)
    degs = [(p - 1) // f for f in factorize(p - 1)]  # факторизация фи(p) = p-1
    answer = []
    for g in range(1, p):
        if all([pow(g, d, p) != 1 for d in degs]):
            answer.append(g)
            if len(answer) == count:
                break
    return answer


def square_root(n):
    x1 = n
    x2 = int((x1 + (n / x1)) / 2)
    while x2 < x1:
        x1, x2 = x2, int((x2 + (n / x2)) / 2)
    return x1


def shanks(m, g, h):
    # Step 1
    r = square_root(m) + 1
    pairs = {pow(g, a, m): a for a in range(r)}
    # Step 2
    g1 = pow(utils.inverse(g, m), r, m)
    for b in range(r):  # r-1 ?
        value = (pow(g1, b, m) * h) % m
        if value in pairs:
            return pairs[value] + r * b


def equation(a, b, m):
    # ax = b (mod m)
    a, b = a % m, b % m
    d = math.gcd(a, m)  # число решений
    if b % d != 0:
        return  # нет решений, если d не делит b

    a_new, b_new, m_new = a // d, b // d, m // d
    d_new, q, r = euclid.euclid_extended(a_new, m_new)  # 1 = a * q + m * r
    q, r = q % m, r % m

    x0 = (b_new * q) % m_new
    for j in range(d):
        yield x0 + m_new * j


def next_yab(y, a, b, params):
    g, h, m = params
    if y <= m // 3:
        y = (y * h) % m
        a = (a + 1) % (m - 1)
    elif m // 3 < y <= 2 * m // 3:
        y = (y * y) % m
        a = (a * 2) % (m - 1)
        b = (b * 2) % (m - 1)
    elif 2 * m // 3 < m:
        y = (y * g) % m
        b = (b + 1) % (m - 1)
    return y, a, b


def ppollard(m, g, h, e=0.05):
    # Step 1
    t = square_root(2 * m * math.log(1 / e)) + 1

    while True:
        # Step 2
        i = 1
        s = random.randint(0, m - 2)    # m-1 ?

        yi, ai, bi = next_yab(pow(g, s, m), 0, s, (g, h, m))
        y2i, a2i, b2i = next_yab(yi, ai, bi, (g, h, m))

        # Step 4
        while i < t and yi != y2i:
            # Step 3
            i += 1
            yi, ai, bi = next_yab(yi, ai, bi, (g, h, m))
            y2i, a2i, b2i = next_yab(*next_yab(y2i, a2i, b2i, (g, h, m)), (g, h, m))

        if yi == y2i:
            # Step 5
            aa, bb = (a2i - ai) % (m - 1), (bi - b2i) % (m - 1)  # h^aa = g^bb
            d = sympy.gcd(aa, m - 1)
            if d < square_root(m - 1):
                for x in equation(aa, bb, m - 1):
                    if pow(g, x, m) == h:
                        return x


def test_accuracy(m, g, h):
    print('Тест корректности алгоритмов')
    print('Образующая g =', g)
    print('Порядок подгруппы m =', m)
    print('Значение степени h =', h)

    for (func, func_name) in [(shanks, 'Алгоритм Шенкса'), (ppollard, 'p-метод Полларда')]:
        x = func(m, g, h)
        if x is not None:
            assert h == pow(g, x, m)
        print('{}: {}'.format(func_name, x if x is not None else 'ответ не найден'))


def test_speed(m, g, h):
    print('Тест скорости работы алгоритмов на 1000 запусков')
    print('Образующий g =', g)
    print('Порядок подгруппы m =', m)
    print('Значение степени h =', h)

    for (func, func_name) in [(shanks, 'Алгоритм Шенкса'), (ppollard, 'p-метод Полларда')]:
        start = time.time()
        for _idx in range(1000):
            func(m, g, h)
        print('{}: {:.3f}c'.format(func_name, time.time() - start))


if __name__ == '__main__':
    """
        -p генерация примитивных корней 
        logarithm.py -p 55609 10
        -a корректность
        logarithm.py -a 17 3 13
        -s скорость работы
        logarithm.py -s 17 3 13
    """
    if sys.argv[1] in ('-a', '-s'):
        test_m = int(sys.argv[2])
        test_g = int(sys.argv[3]) % test_m
        test_h = int(sys.argv[4]) % test_m
        test_func = test_accuracy if sys.argv[1] == '-a' else test_speed
        test_func(test_m, test_g, test_h)
    elif sys.argv[1] == '-p':
        test_m = int(sys.argv[2])
        test_count = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        # print('Первые {} образующих группы порядка m = {}:'.format(test_count, test_m))
        print(primitive_root(test_m, test_count))

# 2163547 3 7 11 12 18 19 28 29
# 89765387 2 5 6 8 14 15 18 22
# 5471 7, 13, 14, 17, 21, 26, 28, 33, 34, 35
