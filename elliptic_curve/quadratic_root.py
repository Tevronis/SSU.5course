import sympy


def legendre_symbol(a, p):
    if a % p == 0:
        return 0
    if a == 1:
        return 1
    if a & 1 == 0:
        return legendre_symbol(a // 2, p) * ((-1) ** ((p ** 2 - 1) // 8))
    if a & 1 == 1:
        return legendre_symbol(p % a, a) * ((-1) ** ((a - 1) * (p - 1) // 4))


def quadratic_root(a, q, p):
    x = None
    # 1
    if q % 4 == 3:
        x = (a ** ((q + 1) // 4)) % p
        if (x ** 2) % p == a % p:
            return x
        else:
            return None
    # 2
    if q % 8 == 5:
        b = a ** ((q + 3) // 8) % p
        c = a ** ((q - 1) // 4) % p
        if c != 1:
            i = 2 ** ((q - 1) // 4) % p
            x = [b * i % p, -(b * i % p)]
        if c == 1:
            x = [b, -b]
        return x
    if q % 16 == 9:  # возможно не работает. Алгоритм 7.5.2.
        b = a ** ((q + 7) // 16) % p
        c = a ** ((q - 1) // 8) % p
        if c != 1:
            i = 2 ** ((q - 1) // 4) % p
            x = [b * i % p, -(b * i % p)]
        if c == 1:
            x = [b, -b]
        return x
    # 3 не понял
    # for b in range(1, p):
    #     e = b ** 2 - 4 * a
    # 4
    if q & 1 == 0:
        return a ** (q // 2) % p





if __name__ == '__main__':
    pass
    # a = 11
    # q = 19
    # p = 19
    # for params in [[11, 19, 19], [21, 37, 37],
    #                [37, 41, 41]]:
    #     print(quadratic_root(*params))

