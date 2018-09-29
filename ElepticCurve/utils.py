import sympy


def get_prime(l):
    #return 65129
    res = sympy.randprime(2 ** l, 2 ** (l + 1))
    return res


def shanks_tonally(n, p):
    n = n % p
    s = p - 1
    r = 0
    # получаем разложение p-1
    while s % 2 == 0:
        s //= 2
        r += 1
    # начальные значения: λ и ω
    l = pow(n, s, p)
    w = pow(n, (s + 1) // 2, p)
    # находим порядок λ
    mod = l
    m = 0
    while mod != 1:
        mod = mod * mod % p
        m += 1
    # находим квадратичный невычет
    z = 0
    for i in range(1, 1000000):
        if legendre_symbol(i, p) == -1:
            z = i
            break
    # находим коэф-ты, на которые будем умножать
    yd_l = pow(pow(z, s, p), pow(2, r - m), p)
    yd_w = pow(pow(z, s, p), pow(2, r - m - 1), p)
    # находим корень
    while l != 1:
        l = l * yd_l % p
        w = w * yd_w % p
    return w


def complex_decomposition(D, p):
    """
    :param D: D > 0
    :param p: simple digit, D = 1
    :return: a, b: p = a^2 + Db^2
    """
    if legendre_symbol(-D, p) == -1:
        return None
    u = shanks_tonally(-D, p)
    i = 0
    u = [u]
    m = [p]
    while True:
        m.append((u[i] * u[i] + D) // m[i])
        u.append(min(u[i] % m[i + 1], (m[i + 1] - u[i]) % m[i + 1]))
        if m[i + 1] == 1:
            assert m[i] == u[i] * u[i] + D
            break
        i += 1
    a = [0] * (i + 1)
    a[i] = u[i]
    b = [0] * (i + 1)
    b[i] = 1
    while True:
        if i == 0:
            a = a[i]
            b = b[i]
            return a, b
        if (-u[i - 1]*a[i] + D*b[i]) % (a[i]*a[i] + D*b[i]*b[i]) == 0:
            a[i - 1] = (-u[i - 1]*a[i] + D*b[i]) // (a[i]*a[i] + D*b[i]*b[i])
        else:
            a[i - 1] = (u[i - 1]*a[i] + D*b[i]) // (a[i]*a[i] + D*b[i]*b[i])
        if (-a[i] - u[i - 1]*b[i]) % (a[i]*a[i] + D*b[i]*b[i]) == 0:
            b[i - 1] = (-a[i] - u[i - 1]*b[i]) // (a[i]*a[i] + D*b[i]*b[i])
        else:
            b[i - 1] = (-a[i] + u[i - 1] * b[i]) // (a[i] * a[i] + D * b[i] * b[i])
        i -= 1


def legendre_symbol(a, p):
    # return sympy.legendre_symbol(a, p)
    if a % p == 0:
        return 0
    if a == 1:
        return 1
    res = pow(a, p - 2, p)
    # assert sympy.legendre_symbol(a, p) == res
    return sympy.legendre_symbol(a, p)
    # if a & 1 == 0:
    #     return legendre_symbol(a // 2, p) * ((-1) ** ((p ** 2 - 1) // 8))
    # if a & 1 == 1:
    #     return legendre_symbol(p % a, a) * ((-1) ** ((a - 1) * (p - 1) // 4))


def jacobi_symbol(m, n):
    return sympy.jacobi_symbol(m, n)


def extended_euclid(a, b):
    if b == 0:
        d = a
        x = 1
        y = 0
        return x, y, d

    x2 = 1
    x1 = 0
    y2 = 0
    y1 = 1
    while b > 0:
        q = a // b
        r = a - q * b
        x = x2 - q * x1
        y = y2 - q * y1
        a = b
        b = r
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y
    d = a
    x = x2
    y = y2
    return x, y, d


def inverse(a, n):
    x, y, d = extended_euclid(a, n)
    if d == 1:
        x = (x % n + n) % n
        return x
    # return pow(a, n - 1, n) если n - простое
    return 0


def test():
    a = 15
    p = 17
    print(legendre_symbol(a, p))
    print(shanks_tonally(7, 127))
    print(complex_decomposition(7, 127))


if __name__ == '__main__':
    test()
