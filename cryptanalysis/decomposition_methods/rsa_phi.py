from math import sqrt


def quadratic_equation(a, b, c):
    d = b*b - 4*a*c
    if d <= 0:
        print('что-то пошло не так')
        exit()
    x1 = int(-b + sqrt(d)) // (2*a)
    x2 = int(-b - sqrt(d)) // (2*a)
    return x1, x2


def decomposition():
    with open('n_phi.txt', 'r') as fin:
        n, phi = map(int, fin.read().split())

    a = 1
    b = -(n - phi + 1)
    c = n
    x1, x2 = quadratic_equation(a, b, c)
    return x1, x2





