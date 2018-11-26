import argparse
import random
import sys

import utils
import elliptic_curve as ec
from elliptic_curve import EllipticPoint as ep


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=int, default=1)
    args = parser.parse_args(sys.argv[1:])

    debug = False
    if args.m == 0:     # Генерация эллиптическрй кривой
        ln = utils.read_param('ln.json', 'ln')
        l = utils.read_param('l.json', 'l')
        p, a, Q, r = ec.generator_elliptic_curve(ln, 30)
        P = ep.mul(Q, l, a, p)
        utils.save_param('curve.json', 'p', p)
        utils.save_param('curve.json', 'Q', (Q.x, Q.y))
        utils.save_param('curve.json', 'a', a)
        utils.save_param('curve.json', 'r', r)
        utils.save_param('P.json', 'P', (P.x, P.y))
        utils.save_param('stat.json', 'stat', 0)

    if args.m == 1 or debug:     # Alice
        if utils.read_param('stat.json', 'stat') == -1:
            raise Exception('Необходимо перегенерировать параметры')
        p = utils.read_param('curve.json', 'p')
        a = utils.read_param('curve.json', 'a')
        r = utils.read_param('curve.json', 'r')
        P = utils.read_param('P.json', 'P')
        l = utils.read_param('l.json', 'l')
        P = ep(p, P[0], P[1])

        k1 = random.randint(2, r)
        k2 = k1 * l % r
        R = ep.mul(P, k1, a, p)
        utils.save_param('secret_key.json', 'k1', k1)
        utils.save_param('secret_key.json', 'k2', k2)
        utils.save_param('R.json', 'R', (R.x, R.y))

    if args.m == 2 or debug:     # Bob
        if utils.read_param('stat.json', 'stat') == -1:
            raise Exception('Необходимо перегенерировать параметры')
        p = utils.read_param('curve.json', 'p')
        a = utils.read_param('curve.json', 'a')
        r = utils.read_param('curve.json', 'r')
        R = utils.read_param('R.json', 'R')
        R = ep(p, R[0], R[1])

        if ep.iszero(ep.mul(R, r, a, p)) and not ep.iszero(R):
            bit = random.randint(0, 1)
            print(bit)
        else:
            raise Exception('rR == Pinf and R is not be equal Pinf')

        utils.save_param('bit.json', 'bit', bit)

    if args.m == 3 or debug:     # Alice
        if utils.read_param('stat.json', 'stat') == -1:
            raise Exception('Необходимо перегенерировать параметры')
        bit = utils.read_param('bit.json', 'bit')
        if bit == 0:
            k = utils.read_param('secret_key.json', 'k1')
            utils.save_param('k.json', 'k', k)
        elif bit == 1:
            k = utils.read_param('secret_key.json', 'k2')
            utils.save_param('k.json', 'k', k)

    if args.m == 4 or debug:
        if utils.read_param('stat.json', 'stat') == -1:
            raise Exception('Необходимо перегенерировать параметры')
        p = utils.read_param('curve.json', 'p')
        a = utils.read_param('curve.json', 'a')
        k = utils.read_param('k.json', 'k')

        R = utils.read_param('R.json', 'R')
        R = ep(p, R[0], R[1])
        Q = utils.read_param('curve.json', 'Q')
        Q = ep(p, Q[0], Q[1])
        P = utils.read_param('P.json', 'P')
        P = ep(p, P[0], P[1])

        bitt = utils.read_param('bit.json', 'bit')

        if bitt == 0:
            if ep.mul(P, k, a, p) == R:
                gd = utils.read_param('stat.json', 'stat')
                gd += 1
                log = 1 - 1 / pow(2, gd)
                utils.save_param('stat.json', 'stat', gd)
                print('Претендент подтвердил что вероятно знает логарифм')
                print('Знает логарифм с верояностью {}'.format(log))
            else:
                utils.save_param('stat.json', 'stat', -1)
                print('Не верно')
        else:
            if ep.mul(Q, k, a, p) == R:
                gd = utils.read_param('stat.json', 'stat')
                gd += 1
                log = 1 - 1 / pow(2, gd)
                utils.save_param('stat.json', 'stat', gd)
                print('Претендент подтвердил что вероятно знает логарифм')
                print('Знает логарифм с верояностью {}'.format(log))
            else:
                utils.save_param('stat.json', 'stat', -1)
                print('Не верно')


if __name__ == '__main__':
    main()
