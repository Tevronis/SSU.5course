import numpy

import utils
import sympy
from math import log2


def primitive_root(m, n):
    for w in range(2, m):
        if pow(w, n, m) != 1:
            continue
        flag = True
        for i in range(1, n):
            flag &= (pow(w, i, m) != 1)
        if not flag:
            continue
        for i in range(1, n):
            res = 0
            for j in range(0, n):
                res = (res + pow(w, i * j)) % m
            flag &= (res == 0)
            if not flag:
                break
        if not flag:
            continue
        return w


def fft(a, m, n, k):
    w = primitive_root(m, n)
    r = {(0, k): a}
    for s in range(k - 1, -1, -1):
        t = 0
        while t < n - 1:
            a_new = [r[(t, s + 1)][j] for j in range(pow(2, s + 1))]
            e = int(bin(t // pow(2, s))[2:].zfill(k)[::-1], 2)
            r[(t, s)] = [(a_new[j] + pow(w, e) * a_new[j + pow(2, s)]) % m for j in range(pow(2, s))]
            r[(t + pow(2, s), s)] = [(a_new[j] + pow(w, e + n // 2) * a_new[j + pow(2, s)]) % m for j in
                                     range(pow(2, s))]
            t += pow(2, s + 1)
    b = [0] * n
    for i in range(n):
        b[int(bin(i)[2:].zfill(k)[::-1], 2)] = r[(i, 0)][0]
    print('Вектор b = {}'.format(str(b)))
    return b


def ifft(b, m, n, k):
    w = utils.inverse(primitive_root(m, n), m) % m
    r = {(0, k): b}
    for s in range(k - 1, -1, -1):
        t = 0
        while t < n - 1:
            b_new = [r[(t, s + 1)][j] for j in range(pow(2, s + 1))]
            e = int(bin(t // pow(2, s))[2:].zfill(k)[::-1], 2)
            r[(t, s)] = [(b_new[j] + pow(w, e) * b_new[j + pow(2, s)]) % m for j in range(pow(2, s))]
            r[(t + pow(2, s), s)] = [(b_new[j] + pow(w, e + n // 2) * b_new[j + pow(2, s)]) % m for j in
                                     range(pow(2, s))]
            t += pow(2, s + 1)
    a = [0] * n
    for i in range(n):
        # print(int(bin(i)[2:].zfill(k)[::-1], 2))
        # print(utils.inverse(m, n % m))
        a[int(bin(i)[2:].zfill(k)[::-1], 2)] = (utils.inverse(n % m, m) * r[(i, 0)][0]) % m
    print('Вектор a = {}'.format(str(a)))


def interpolate_lagrange_polynomial(x, x_values, y_values, size):
    lagrange_pol = 0
    for i in range(size):
        basics_pol = 1
        for j in range(size):
            if j == i:
                continue
            basics_pol *= (x - x_values[j]) // (x_values[i] - x_values[j])

        lagrange_pol += basics_pol * y_values[i]
    return lagrange_pol


def plot(values):
    import matplotlib.pyplot as plt
    X = [item[0] for item in values if item[0] != -1]
    Y = [item[1] for item in values if item[1] != -1]

    plt.plot(X, Y)
    plt.show()


def test_lagrange():
    size = 10
    # x_values = list(map(int, input().split()))
    # y_values = list(map(int, input().split()))
    x_values = []
    y_values = []
    for i in range(size):
        x_values.append(i)
        y_values.append(i**3 + 3*i*i + 3*i + 1)
    dots = []
    x = 0
    for i in range(1000):
        x += 0.5
        y = interpolate_lagrange_polynomial(x, x_values, y_values, size)
        dots.append([x, y])
    plot(dots)


if __name__ == '__main__':
    # test_lagrange()
    m = int(input('Модуль m = '))
    a = list(map(int, input('Вектор a = ').split()))
    if m % 2 == 0 or not sympy.isprime(m):
        print('Введено неправильное значение модуля m')
        exit()
    n = len(a)
    for i in range(n):
        if not 0 <= a[i] <= m - 1:
            print('Введено неправильное значение вектора a')
            exit()

    k = int(log2(n))
    if 2 ** k != n:
        print('Введено неправильное количество значений вектора a')
        exit()
    cmd = input('cmd [f/i]: ')
    if cmd == 'f':
        fft(a, m, n, k)
    elif cmd == 'i':
        ifft(a, m, n, k)
    elif cmd == 'l':
        test_lagrange()
