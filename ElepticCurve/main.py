# -*- coding: utf-8 -*-
import sys
from time import time

from elliptic_curve import EllipticPoint, generator_elliptic_curve


def plot(values):
    import matplotlib.pyplot as plt
    X = [item[0] for item in values if item[0] != -1]
    Y = [item[1] for item in values if item[1] != -1]

    plt.scatter(X, Y, s=1)
    plt.show()


def main(args):
    if len(args) == 1:
        l, m = 13, 72
    else:
        l, m = map(int, args[1:])
    start = time()
    p, A, Q, r = generator_elliptic_curve(l, m)
    print('Time to gen:', time() - start)
    # p = 773
    # A, Q, r = 78, EllipticPoint(p, 117, 386), 408
    dots = [Q]
    print("p: {}, A: {}, Q: {}, r: {}".format(p, A, Q.__repr__(), r))
    print('Q * r:', EllipticPoint.mul(Q, r * r, A, p))
    if l < 20:
        for i in range(r - 1):
            pp = EllipticPoint.sum(Q, dots[i], A, p)
            dots.append(pp)
        dots = [[item.x, item.y] for item in dots]
        assert r == len(dots)
        open('dots.txt', 'w').write(''.join(list(map(str, dots))))
        plot(dots)


if __name__ == '__main__':
    main(sys.argv)
