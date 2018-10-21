import itertools
from time import time


def euclid(a, b):
    if not 0 < b <= a:
        return False
    # assert 0 < b <= a
    r = [a, b]
    i = 1
    while True:
        r.append(r[i - 1] % r[i])
        if r[i + 1] == 0:
            d = r[i]
            break
        i += 1
    return d


def euclid_bin(a, b):
    if not 0 < b <= a:
        return False
    assert 0 < b <= a
    g = 1
    while a % 2 == 0 and b % 2 == 0:
        a >>= 1
        b >>= 1
        g <<= 1
    u = a
    v = b
    while u != 0:
        while u % 2 == 0:
            u >>= 1
        while v % 2 == 0:
            v >>= 1
        if u >= v:
            u = u - v
        else:
            v = v - u
    d = g * v
    return d


def euclid_extended(a, b):
    if not 0 < b <= a:
        return False
    r = [a, b]
    x = [1, 0]
    y = [0, 1]
    i = 1
    q = [0]
    while True:
        q.append(r[i - 1] // r[i])
        r.append(r[i - 1] % r[i])
        if r[i + 1] == 0:
            d = r[i]
            X = x[i]
            Y = y[i]
            break
        else:
            x.append(x[i - 1] - q[i] * x[i])
            y.append(y[i - 1] - q[i] * y[i])
            i += 1
    return d, X, Y


def euclid_time_test(a, b):
    start = time()
    for t in range(1000000):
        euclid(a, b)
    print('Время выполнениея обычного алгоритма Евклида: ', time() - start)

    start = time()
    for t in range(1000000):
        euclid_bin(a, b)
    print('Время выполнения бинарного алгоритма Евклида: ', time() - start)

    start = time()
    for t in range(1000000):
        euclid_extended(a, b)
    print('Время выполнения расширенного алгоритма Евклида: ', time() - start)


def euclid_distance_test(d1, d2):
    s = range(d1, d2)
    f = range(d1, d2)
    start = time()
    for a, b in itertools.product(s, f):
        euclid(a, b)
    print('Время выполнениея обычного алгоритма Евклида: ', time() - start)

    start = time()
    for a, b in itertools.product(s, f):
        euclid_bin(a, b)
    print('Время выполнения бинарного алгоритма Евклида: ', time() - start)

    start = time()
    for a, b in itertools.product(s, f):
        euclid_extended(a, b)
    print('Время выполнения расширенного алгоритма Евклида: ', time() - start)


def main():
    euclid_time_test(321, 123)
    euclid_time_test(16777217, 1023)
    euclid_distance_test(1, 1000)
    euclid_distance_test(20000, 21000)


if __name__ == '__main__':
    main()
