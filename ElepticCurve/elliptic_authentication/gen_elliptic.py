import utils
import elliptic


def elliptic_gen(l, m):
    """step 1"""
    while True:
        p = utils.find_prime(l)

        """step 2"""
        c, d = utils.complex_decomposition(3, p)
        assert c*c+3*d*d == p

        """step 3"""
        T = [c + 3 * d, -c - 3 * d, c - 3 * d, -c + 3 * d, 2 * c, -2 * c]
        r = None
        for t in T:
            N = p + 1 + t
            if utils.isprime(N):
                r = N
                break
            if N % 2 == 0 and utils.isprime(N // 2):
                r = N // 2
                break
            if N % 3 == 0 and utils.isprime(N // 3):
                r = N // 3
                break
            if N % 6 == 0 and utils.isprime(N // 6):
                r = N // 6
                break
        if r is None:
            continue

        """step 4"""
        good = True
        for i in range(1, m):
            if (p ** i) % r == 1:
                good = False
        if p == r or not good:
            continue
        break

    """step 5"""
    while True:
        e = elliptic.gen_ellip_point(p)
        B = (e[1] * e[1] - e[0] * e[0] * e[0]) % p
        f = False
        if N == r:
            if utils.legendre_symbol(B, p) == -1 and utils.legendre_symbol(B, p, 3) == -1:
                f = True
        if N == 6*r:
            if utils.legendre_symbol(B, p) == 1 and utils.legendre_symbol(B, p, 3) == 1:
                f = True
        if N == 2*r:
            if utils.legendre_symbol(B, p) == -1 and utils.legendre_symbol(B, p, 3) == 1:
                f = True
        if N == 3*r:
            if utils.legendre_symbol(B, p) == 1 and utils.legendre_symbol(B, p, 3) == -1:
                f = True
        if f is False:
            continue

        """step 6"""
        m = elliptic.mul(e, N, 0, p)
        if m == [-1, -1]:
            break

    """step 7"""
    Q = elliptic.mul(e, N//r, 0, p)

    return p, B, Q, r


def is_curve_dot(Q, p, B):
    a = Q[0]
    b = Q[1]
    e = elliptic.gen_ellip_point(p, a, b)
    if B == (e[1] * e[1] - e[0] * e[0] * e[0]) % p:
        return True


def gen_el_curve(l):
    m = utils.get_m(l)
    p, B, Q, r = elliptic_gen(l, m)
    assert elliptic.mul(Q, r, 0, p) == [-1, -1]
    return p, B, Q, r
