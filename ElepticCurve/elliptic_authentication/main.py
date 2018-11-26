import argparse
import sys
import random
import elliptic
import gen_elliptic
import utils

"""СТРАНИЦА 285"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=int, default=1)
    args = parser.parse_args(sys.argv[1:])

    if args.m == 0:
        l = int(open('len.txt').read().strip())
        p, B, a, r = gen_elliptic.gen_el_curve(l)
        open('p.txt', 'w').write(str(p))
        open('B_coefficient.txt', 'w').write(str(B))
        open('a.txt', 'w').write('{} {}'.format(a[0], a[1]))
        open('r.txt', 'w').write(str(r))

    if args.m == 1:
        r = int(open('r.txt').read().strip())
        a = list(map(int, open('a.txt').read().strip().split()))
        p = int(open('p.txt').read().strip())
        x = random.randint(2, r)
        b = elliptic.mul(a, x, 0, p)
        k = 1
        open('k.txt', 'w').write(str(k))
        open('x_secret_key.txt', 'w').write(str(x))
        open('b.txt', 'w').write('{} {}'.format(b[0], b[1]))

    if args.m == 2:
        x = int(open('x_secret_key.txt').read().strip())
        r = int(open('r.txt').read().strip())
        a = list(map(int, open('a.txt').read().strip().split()))
        p = int(open('p.txt').read().strip())
        k = int(open('k.txt').read().strip())

        if k == 0:
            print('необходимо перегенерировать параметры!')
            input()
            exit()
        else:
            y = x
            while y == x:
                y = random.randint(2, r)
            c = elliptic.mul(a, y, 0, p)
            open('y.txt', 'w').write(str(y))
            open('c.txt', 'w').write('{} {}'.format(c[0], c[1]))

    if args.m == 3:
        c = list(map(int, open('c.txt').read().strip().split()))
        p = int(open('p.txt').read().strip())
        B = int(open('B_coefficient.txt').read().strip())
        k = int(open('k.txt').read().strip())

        if k == 0:
            print('необходимо перегенерировать параметры!')
            input()
            exit()
        else:
            if not gen_elliptic.is_curve_dot(c, p, B):
                print('не существует такой точки на заданной эллиптической кривой')
                input()
                exit()
            else:
                bitt = random.randint(0, 1)
                open('bit.txt', 'w').write(str(bitt))

    if args.m == 4:
        bitt = int(open('bit.txt').read().strip())
        r = int(open('r.txt').read().strip())
        y = int(open('y.txt').read().strip())
        x = int(open('x_secret_key.txt').read().strip())
        k = int(open('k.txt').read().strip())

        if k == 0:
            print('необходимо перегенерировать параметры!')
            input()
            exit()
        else:
            if bitt == 0:
                open('log.txt', 'w').write(str(y))
            else:
                k = (y * utils.inverse(x, r)) % r
                open('log.txt', 'w').write(str(k))

    if args.m == 5:
        bitt = int(open('bit.txt').read().strip())
        ans = int(open('log.txt').read().strip())
        p = int(open('p.txt').read().strip())
        k = int(open('k.txt').read().strip())
        a = list(map(int, open('a.txt').read().strip().split()))
        b = list(map(int, open('b.txt').read().strip().split()))
        c = list(map(int, open('c.txt').read().strip().split()))
        k = int(open('k.txt').read().strip())

        if k == 0:
            print('необходимо перегенерировать параметры!')
            input()
            exit()
        else:
            if bitt == 0:
                if elliptic.mul(a, ans, 0, p) == c:
                    l = 1 - 1/pow(2, k)
                    print('знает логарифм с верояностью {}'.format(l))
                    k = k+1
                    open('k.txt', 'w').write(str(k))
                    input()
                    exit()
                else:
                    k = 0
                    open('k.txt', 'w').write(str(k))
                    print('не верно')
                    input()
                    exit()

            else:
                if elliptic.mul(b, ans, 0, p) == c:
                    l = 1 - 1/pow(2, k)
                    print('знает логарифм с верояностью {}'.format(l))
                    k = k+1
                    open('k.txt', 'w').write(str(k))
                    input()
                    exit()
                else:
                    k = 0
                    open('k.txt', 'w').write(str(k))
                    print('не верно')
                    input()
                    exit()


if __name__ == '__main__':
    main()




















