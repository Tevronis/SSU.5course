import sympy

from elliptic_curve import EllipticPoint

from utils import get_prime, complex_decomposition, inverse, legendre_symbol


def generator_elliptic_curve(l, m, prt=False):
    # 1) p = 1 (mod 4), len(p) == l, p - simple
    while True:
        if prt: print('Step 1.')
        while True:
            p = get_prime(l)
            if p % 4 == 1:
                break
        print('prime genned')

        # 2) fac = factor(p)
        if prt: print('Step 2.')
        a, b = complex_decomposition(1, p)
        assert a * a + b * b == p
        # 3) N = p + 1 + T; T = +-{2a, 2b}
        # __ if N == 2r or N == 4r (r - simple)
        # __ if not -> step 1
        if prt: print('Step 3.')
        T = [-2 * a, -2 * b, 2 * a, 2 * b]
        for t in T:
            N = p + 1 + t
            if sympy.isprime(N // 2):
                r = N // 2
                break
            if sympy.isprime(N // 4):
                r = N // 4
                break
        else:
            continue

        # 4) if p != r and p^i != 1 (mod r) i = 1..m
        # __ if not -> step 1
        if prt: print('Step 4.')
        good = True
        for i in range(1, m):
            if (p ** i) % r == 1:
                good = False
        if p == r or not good:
            continue
        # 5) generate (x0, y0): x0 != 0, y0 != 0
        # __ A=(y0^2 - x0^3)*x0^-1 (mod p)
        # if -A квадратичный невычет для N=2r
        # __ -A квадратичный вычет для N = 4r
        # if not -> step 5
        if prt: print('Step 5.')
        while True:
            # e = EllipticPoint()  # EllipticPoint(1, 2)
            e = EllipticPoint.rand_point(p)
            A = ((e.y ** 2 - e.x ** 3) * inverse(e.x, p)) % p
            good = False
            if N == r * 2:
                # j = sympy.legendre_symbol(-A, p)
                # jj = legendre_symbol(-A, p)
                if legendre_symbol(-A, p) == -1:
                    good = True
            if N == r * 4:
                if legendre_symbol(-A, p) == 1:
                    good = True
            if not good:
                continue

            # 6) if N * (x0, y0) == Pinf
            # if not -> step 5
            # W = EllipticPoint.mul(e, 2, aa, p)
            # WW = EllipticPoint.sum(W, e, aa, p)
            m = EllipticPoint.mul(e, N, A, p)
            if m == EllipticPoint.getinf():  # == !!!!!!!!!!!!!!
                print('kekas')
                break
        # 7) Q = N/r * (x0, y0)
        Q = EllipticPoint.mul(e, N // r, A, p)
        # 8) return (p, A, Q, r)
        return p, A, Q, r


def plot(values):
    import matplotlib.pyplot as plt
    X = [item[0] for item in values]
    Y = [item[1] for item in values]

    plt.scatter(X, Y, s=2)
    plt.show()


def main():
    # j = 1728
    # l = int(input('Характеристика поля: '))
    # m = int(input('Максимальная степень расширения: '))
    # aa = int(input('a (хз что это но нужно): '))
    l = 512
    m = 72

    # for i in range(200):
    p, A, Q, r = generator_elliptic_curve(l, m)
    dots = [Q]
    print("p: {}, A: {}, Q: {}, r: {}".format(p, A, Q.__repr__(), r))
    print(EllipticPoint.mul(Q, r, A, p))
    # for i in range(5000):
    #     pp = EllipticPoint.sum(Q, dots[i], a, p)
    #     dots.append(pp)
    # dots.append([Q.x, Q.y])
    # dots = [[item.x, item.y] for item in dots]
    # plot(dots)


if __name__ == '__main__':
    main()
