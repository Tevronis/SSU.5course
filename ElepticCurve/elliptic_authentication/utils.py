import random


def get_m(l):
    if l < 5:
        return 2
    if l < 20:
        return 4
    if l < 100:
        return 12
    if l < 150:
        return 24
    if l < 200:
        return 39
    if l < 250:
        return 58
    if l < 300:
        return 78
    if l < 350:
        return 103
    if l >= 350:
        return 129


def find_prime(l):
    while True:
        p = random.randint(2 ** (l - 1), 2 ** l)
        if p % 2 == 0:
            p += 1
        while p < 2**l:
            if p % 6 == 1 and isprime(p):
                return p
            else:
                p = p + 2


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


def sh_t(n, p):
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
    :param p: simple digit, D = 3
    :return: a, b: p = a^2 + Db^2
    """
    if legendre_symbol(-D, p) == -1:
        return None
    u = sh_t(-D, p)
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


def legendre_symbol(B, p, d=2):
    if B % p == 0:
        return 0
    if B == 1:
        return 1
    res = pow(B, (p - 1) // d, p)
    if res != 1:
        res = -1
    return res


def isprime(n, K=10):
    def getST(t):
        s = 0
        while t % 2 == 0:
                t //= 2
                s += 1
        return s, t

    if n == 2 or n == 3:
        return True

    if n < 2 or n % 2 == 0:
        return False

    s, t = getST(n - 1)
    for k in range(K):
        a = random.randrange(2, n - 2)
        x = pow(a, t, n)
        if x == 1 or x == n - 1:
            continue
        for i in range(1, s):
            x = (x * x) % n
            if x == 1:
                return False
            if x == n - 1:
                break
        if x != n - 1:
            return False
    return True


def inverse(a, n):
    x, y, d = extended_euclid(a, n)
    if d == 1:
        x = (x % n + n) % n
        return x
    return 0