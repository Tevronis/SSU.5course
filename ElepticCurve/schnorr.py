# -*- coding: utf-8 -*-
import hashlib
import random
import sys

from elliptic_curve import generator_elliptic_curve, EllipticPoint as ep
from utils import read_param, save_param

hashf = hashlib.sha256


def key_generation(r, g, a, p):
    Q = g
    x = random.randint(1, r - 1)
    P = ep.mul(Q, x, a, p)
    return x, P, Q


def hsh(m, p, r):
    return int.from_bytes(hashf(m
                                + p.x.to_bytes(p.x.bit_length(), byteorder='big')
                                + p.y.to_bytes(p.y.bit_length(), byteorder='big')).digest(), byteorder='big') % r


def signature(M, Q, a, r, p, x):
    k = random.randint(1, r - 1)
    R = ep.mul(Q, k, a, p)
    e = hsh(M, R, r)

    assert e % r != 0
    s = (x * e + k) % r
    print('Данные подписаны')
    print('m={}, e={}, s={}'.format(M, e, s))
    return e, s, R


def verify(M, P, Q, R, a, p, s, e, r):
    assert R.y ** 2 % p == (R.x ** 3 + a * R.x) % p, print('Точка не принадлежит эллиптической кривой')
    e2 = hsh(M, R, r)
    if ep.mul(Q, s, a, p) == ep.sum(ep.mul(P, e2, a, p), R, a, p):
        print('Подпись действительна')
    else:
        print('Подпись недействительна')
    return e == e2


def create_elliptic():
    l, m = read_param('ln.json', 'ln'), 10
    p, a, G, r = generator_elliptic_curve(l, m)
    return p, a, G, r


def main():
    # 322 страница протокол аутентификации
    m = int(sys.argv[1])     # int(input('m: '))
    debug = False
    if m == 1:
        p, a, G, r = create_elliptic()
        save_param('curve.json', 'p', p)
        save_param('curve.json', 'a', a)
        save_param('curve.json', 'G', (G.x, G.y))
        save_param('curve.json', 'r', r)
    if m == 2 or debug:
        Gp = read_param('curve.json', 'G')
        a = read_param('curve.json', 'a')
        p = read_param('curve.json', 'p')
        r = read_param('curve.json', 'r')
        assert 0 <= Gp[0] < p, 0 <= Gp[1] < p
        g = ep(p, Gp[0], Gp[1])
        x, P, Q = key_generation(r, g, a, p)
        save_param('secret.json', 'x', x)
        save_param('P.json', 'P', (P.x, P.y))
        save_param('Q.json', 'Q', (Q.x, Q.y))
    if m == 3 or debug:
        M = open('file.txt', 'rb').read()
        Qp = read_param('Q.json', 'Q')
        a = read_param('curve.json', 'a')
        r = read_param('curve.json', 'r')
        p = read_param('curve.json', 'p')
        x = read_param('secret.json', 'x')
        Q = ep(p, Qp[0], Qp[1])
        e, s, R = signature(M, Q, a, r, p, x)
        save_param('signature.json', 'e', e)
        save_param('signature.json', 's', s)
        save_param('signature.json', 'R', (R.x, R.y))
    if m == 4 or debug:
        M = open('file.txt', 'rb').read()
        a = read_param('curve.json', 'a')
        r = read_param('curve.json', 'r')
        p = read_param('curve.json', 'p')
        s = read_param('signature.json', 's')
        e = read_param('signature.json', 'e')
        Qp = read_param('Q.json', 'Q')
        Rp = read_param('signature.json', 'R')
        Pp = read_param('P.json', 'P')
        Q = ep(p, Qp[0], Qp[1])
        R = ep(p, Rp[0], Rp[1])
        P = ep(p, Pp[0], Pp[1])
        result = verify(M, P, Q, R, a, p, s, e, r)
        save_param('result.json', 'result', result)


if __name__ == '__main__':
    main()
