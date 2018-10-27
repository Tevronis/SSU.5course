import argparse
import hashlib
import json
import sys

import utils
from utils import read_param, save_param, write_log, isprime


def get_public_params(len_p):
    assert len_p % 64 == 0
    assert 512 <= len_p <= 1024

    while True:
        q = utils.get_big_prime(2 ** (160 - 1), 2 ** 160)
        p = q * (2 ** (len_p - 160))
        # print('p:', len(bin(p)[2:]), 'bit')
        high = 2 ** len_p
        # print('high:', len(bin(high)[2:]), 'bit')
        while p < high:
            p += q
            if not isprime(p + 1):
                continue
            p += 1
            if (p - 1) % q == 0:
                break
        if isprime(p):
            break
    # print(p)
    # print('p:', len(bin(p)[2:]), 'bit')
    h = 2
    while not pow(h, (p - 1) // q, p) > 1:
        h += 1
    g = pow(h, (p - 1) // q, p)

    return p, q, g


def get_private_params(p, q, g):
    x = utils.get_big_digit(1, q)
    y = pow(g, x, p)
    return x, y


def get_hash(data):
    result = ''
    x = hashlib.sha1(data).digest()
    w = list(map(int, x))
    for item in w:
        b = bin(item)[2:]
        b = str(b).rjust(8, '0')
        result += b
    return int(result, 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=int, default=1)
    args = parser.parse_args(sys.argv[1:])
    with open('file_to_signature.txt') as f:
        file = json.load(f)

    m = open(file['file'], 'rb').read()

    if args.m == 1:  # публичные параметры
        len_p = read_param('len_p.j', 'l')
        p, q, g = get_public_params(len_p)
        save_param('p.json', 'p', p)
        save_param('q.json', 'q', q)
        save_param('g.json', 'g', g)
    elif args.m == 2:  # частные парметры
        p = read_param('p.json', 'p')
        q = read_param('q.json', 'q')
        g = read_param('g.json', 'g')
        x, y = get_private_params(p, q, g)
        save_param('x.json', 'x', x)
        save_param('y.json', 'y', y)
    elif args.m == 3:  # Алиса генерит k < q
        q = read_param('q.json', 'q')
        k = utils.get_big_prime(2, q)
        save_param('k.json', 'k', k)
    # elif args.m == 4:  # Алиса подписывает
        g = read_param('g.json', 'g')
        k = read_param('k.json', 'k')
        p = read_param('p.json', 'p')
        q = read_param('q.json', 'q')
        x = read_param('x.json', 'x')
        r = pow(g, k, p) % q
        s = (utils.inverse(k, q) * (get_hash(m) + x * r)) % q
        save_param('signature.json', 'r', r)
        save_param('signature.json', 's', s)
    elif args.m == 4:  # боб проверяет
        s = read_param('signature.json', 's')
        r = read_param('signature.json', 'r')
        q = read_param('q.json', 'q')
        p = read_param('p.json', 'p')
        g = read_param('g.json', 'g')
        y = read_param('y.json', 'y')
        w = utils.inverse(s, q)
        u1 = get_hash(m) * w % q
        u2 = r * w % q
        v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
        save_param('v.json', 'v', v)
        if v == r:
            print("Подпись верна")
            input()
        else:
            print("Подпись не верна")
    # 2.3
    else:
        write_log('Bad args')


if __name__ == '__main__':
    main()
