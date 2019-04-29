import collections
from math import sqrt

import vigenere


def open_table(text, alf):
    result = collections.Counter()
    text = text.lower()
    for item in text:
        if item in alf:
            result[item] += 1
    res_len = sum(result.values())
    for item in result:
        result[item] = result[item] / res_len
    result = sorted(result.items(), key=lambda x: -x[1])
    return result


def get_h0(text, alph):
    m = len(alph)
    freqs = open_table(text, alph)
    freqs = [(char, float(value)) for char, value in freqs]
    h0 = [[letter, 0] for letter in alph]
    for i in range(m):
        for k in range(m):
            j = (i - k) % m
            h0[j][1] += freqs[i][1] * freqs[k][1]
    h0 = [(char, '{:.5f}'.format(freq)) for char, freq in h0]
    return freqs, h0


def get_hd(enc, alph, d):
    n = len(enc)
    while n % d:
        n -= 1
    t, r = n // d, (len(enc)) - n

    z = ''
    for idx in range((t - 1) * d + r):
        idx_next = idx + d
        if enc[idx] in alph and enc[idx_next] in alph:
            letter = alph[(alph.index(enc[idx]) - alph.index(enc[idx_next])) % len(alph)]
            z += letter
    hd = [(letter, z.count(letter) / len(z)) for letter in alph]
    return hd


def get_norm(x):
    return sqrt(sum(map(lambda xi: xi ** 2, x)))


def get_distance(x, y):
    return get_norm([yi - xi for xi, yi in zip(x, y)])


def main():
    op = input('1. шифрование\n2. расшифровка\n3. h0\n4. hd\n> ')
    if op == '1':
        textname = input('введите название файла\n> ')
        alph = open('alphabet.txt').read()
        key = open('key.txt').read()
        text = vigenere.del_not_alf(open(textname).read(), alph)
        crypt = vigenere.vigenere_encryption(text, key, alph)
        open('crypt.txt', 'w').write(crypt)
        print('сохранен файл: crypt.txt')
    elif op == '2':
        text = open('crypt.txt', 'r').read()
        key = open('key.txt').read().strip()
        alf = open('alphabet.txt', 'r').read()
        decrypt = vigenere.vigenere_decryption(text, key, alf)
        open('decrypt.txt', 'w').write(str(decrypt))
        print('сохранен файл: decrypt.txt')
    elif op == '3':
        textname = input('название файла\n> ')
        text = open(textname).read().lower()
        alph = open('alphabet.txt', 'r').read()
        freqs, h0 = get_h0(text, alph)

        with open('f.txt', 'w') as fout:
            for k, v in freqs:
                fout.write('{} {}\n'.format(k, v))
        with open('h0.txt', 'w') as fout:
            for k, v in h0:
                fout.write('{} {}\n'.format(k, v))

    elif op == '4':
        enc = open('crypt.txt', 'r').read()
        h0 = []
        with open('h0.txt') as f:
            for line in f:
                char, value = line[0], line[2:]
                h0.append((char, float(value)))
        alph = ''.join(map(lambda h0i: h0i[0], h0))
        n1 = int(input('введите n1\n> '))
        n2 = int(input('введите n2\n> '))

        hds = [get_hd(enc, alph, d) for d in range(n1, n2 + 1)]
        n_min, dist_min = None, 1
        for idx, hd in enumerate(hds):
            dist = get_distance(
                list(map(lambda xi: float(xi[1]), h0)),
                list(map(lambda yi: yi[1], hd)))
            if dist < dist_min:
                n_min, dist_min = n1 + idx, dist
            print(n1 + idx, ':', dist)
        print('Наименьшее расстояние до H0 при d =', n_min)


if __name__ == '__main__':
    main()
