import hashlib
import random

from elliptic_curve import generator_elliptic_curve, EllipticPoint as ep
from utils import inverse, read_param, save_param

hashf = hashlib.sha256


def key_generation(G, a, p, n):
    k = random.randint(1, n - 1)  # private key
    A = ep.mul(G, k, a, p)
    print('Сгенерирован секретный и  публичный ключ (k, A)')
    print('k={}, A={}'.format(k, A))
    return k, A


def hsh(m, p):
    return int.from_bytes(hashf(m).digest(), byteorder='big') % p


def signature(M, G, a, n, p, x):
    r, k, R = 0, None, None
    while r == 0:
        k = random.randint(1, n - 1)
        R = ep.mul(G, k, a, p)
        r = R.x % p

    e = hsh(M, n)
    assert 0 <= e < n
    s = (e + r*x) * inverse(k, n) % n
    print('Данные подписаны')
    print('R={}, s={}'.format(R, s))
    return R, s


def verify(M, R, s, a, p, A, G, n):
    assert 1 <= s <= p
    assert R.y ** 2 % p == (R.x ** 3 + a * R.x) % p, print('Точка не принадлежит эллиптической кривой')
    V1 = ep.mul(R, s, a, p)
    V2 = ep.sum(ep.mul(G, hsh(M, n), a, p), ep.mul(A, R.x, a, p), a, p)
    if V1 == V2:
        print('Подпись верна')
    else:
        print('Подпись не верна')
    return V1 == V2


def create_elliptic():
    l, m = int(open('l.json').read()), 10
    p, a, G, r = generator_elliptic_curve(l, m)
    return p, a, G, r


def main():
    # 322 страница протокол аутентификации
    m = int(input('m: '))
    if m == 1:
        p, a, G, r = create_elliptic()
        save_param('curve.json', 'p', p)
        save_param('curve.json', 'a', a)
        save_param('curve.json', 'G', (G.x, G.y))
        save_param('curve.json', 'r', r)
    elif m == 2:
        Gp = read_param('curve.json', 'G')
        a = read_param('curve.json', 'a')
        p = read_param('curve.json', 'p')
        r = read_param('curve.json', 'r')
        assert 0 <= Gp[0] < p, 0 <= Gp[1] < p
        G = ep(p, Gp[0], Gp[1])
        k, A = key_generation(G, a, p, r)
        save_param('alice_secret_key.json', 'key', k)
        save_param('alice_public_key.json', 'Ax', A.x)
        save_param('alice_public_key.json', 'Ay', A.y)
        save_param('alice_public_key.json', 'p', A.p)
    elif m == 3:
        M = open('file.txt', 'rb').read()
        Gp = read_param('curve.json', 'G')
        a = read_param('curve.json', 'a')
        r = read_param('curve.json', 'r')
        p = read_param('curve.json', 'p')
        x = read_param('alice_secret_key.json', 'key')
        G = ep(p, Gp[0], Gp[1])
        R, s = signature(M, G, a, r, p, x)
        save_param('signature.json', 'R', (R.x, R.y))
        save_param('signature.json', 's', s)
    elif m == 4:
        M = open('file.txt', 'rb').read()
        Rp = read_param('signature.json', 'R')
        s = read_param('signature.json', 's')
        Ax = read_param('alice_public_key.json', 'Ax')
        Ay = read_param('alice_public_key.json', 'Ay')
        Gp = read_param('curve.json', 'G')
        a = read_param('curve.json', 'a')
        p = read_param('curve.json', 'p')
        r = read_param('curve.json', 'r')
        G = ep(p, Gp[0], Gp[1])
        A = ep(p, Ax, Ay)
        R = ep(p, Rp[0], Rp[1])
        result = verify(M, R, s, a, p, A, G, r)
        save_param('result.json', 'result', result)


if __name__ == '__main__':
    main()


