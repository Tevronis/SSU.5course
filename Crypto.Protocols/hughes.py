import argparse
import sys
from math import gcd

import sympy
import utils
from utils import read_param, save_param, write_log


def get_public_params(len_p):
    while True:
        p = utils.get_big_prime(2 ** len_p, 2 ** (len_p + 1))
        if sympy.isprime((p - 1) // 2):
            break
    g = utils.generator(p)
    # print('Сгенерированы параметры \n g: {} \n p: {}'.format(g, p))
    with open('log.log', 'a') as f:
        f.write('Сгенерированы параметры \n\t g: {} \n\t p: {}\n'.format(g, p))
    return g, p


def get_private_params_Alice(p, g):
    while True:
        x = utils.get_big_digit() % p
        if gcd(x, p - 1) == 1 and utils.inverse(x, p - 1) >= 0:
            break
    k = pow(g, x, p)
    with open('log.log', 'a') as f:
        f.write("Алисой вычислен закрытый ключ x: {}\n".format(x))
        f.write("Алисой сгенерирован открытый ключ k: {}\n".format(k))
    return x, k


def get_private_params_Bob(p, g):
    while True:
        y = utils.get_big_digit() % p
        if gcd(y, p - 1) == 1 and utils.inverse(y, p - 1) >= 0:
            break
    d = pow(g, y, p)
    z = utils.inverse(y, p - 1)

    with open('log.log', 'a') as f:
        f.write("Бобом вычислен закрытый ключ y: {}\n".format(y))
        f.write("Бобом вычислен параметр z (обратный элемент к y): {}\n".format(z))
        f.write("Бобом сгенерирован открытый ключ d: {}\n".format(d))
    return y, d, z


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=int, default=1)
    args = parser.parse_args(sys.argv[1:])

    if args.m == 1:
        len_p = read_param('len_p.j', 'l')
        g, p = get_public_params(len_p)
        save_param('g.json', 'g', g)
        save_param('p.json', 'p', p)
    elif args.m == 2:  # Шаг Алисы
        p = read_param('p.json', 'p')
        g = read_param('g.json', 'g')
        x, k = get_private_params_Alice(p, g)
        save_param('x.json', 'x', x)
        save_param('k.json', 'k', k)
    elif args.m == 3:  # Шаг Боба
        p = read_param('p.json', 'p')
        g = read_param('g.json', 'g')
        y, d, z = get_private_params_Bob(p, g)
        save_param('y.json', 'x', y)
        save_param('d.json', 'd', d)
        save_param('z.json', 'z', z)
    elif args.m == 4:  # Шаг Алисы
        d = read_param('d.json', 'd')
        p = read_param('p.json', 'p')
        x = read_param('x.json', 'x')
        m = pow(d, x, p)
        write_log('Алисой вычислен параметр m: {}'.format(m))
        save_param('m.json', 'm', m)  # m == X
    elif args.m == 5:
        z = read_param('z.json', 'z')
        m = read_param('m.json', 'm')
        p = read_param('p.json', 'p')
        k = pow(m, z, p)
        write_log('Бобом вычислен параметр k: {}'.format(k))
        save_param('Bob_key.json', 'k', k)
    else:
        write_log('Bad args')


if __name__ == '__main__':
    # sys.stdout = open('log.log', 'w')
    main()
