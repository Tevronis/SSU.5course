import copy
import functools
import random
from itertools import chain, combinations
from math import sqrt, gcd


def is_b_smooth(p, b):
    alpha = []
    for bi in b:
        k = 0
        while p % bi == 0 and not bi < 0 < p and p != 1:
            p //= bi
            k += 1
        alpha.append(k)
    return p == 1, alpha, [al % 2 for al in alpha]


def gen_fraction(n):
    a0 = sqrt(n)
    r0 = int(a0)
    yield r0
    ratio0 = 1
    chislitel0 = 0

    while True:
        chislitel1 = r0 * ratio0 - chislitel0
        ratio1 = (n - chislitel1 * chislitel1) // ratio0
        if ratio1 == 0:
            raise ValueError('Число - полный квадрат')
        r1 = int((a0 + chislitel1) / ratio1)
        yield r1
        r0, ratio0, chislitel0 = r1, ratio1, chislitel1


def gen_suitable_fractions(n):
    fraction = gen_fraction(n)
    p0 = 1
    p1 = next(fraction)

    while True:
        p2 = next(fraction) * p1 + p0
        yield p2
        p0, p1 = p1, p2


def sum_rows(*rows):
    for row in rows[1:]:
        for idx in range(len(row)):
            rows[0][idx] = (rows[0][idx] + row[idx]) % 2
    return rows[0]


def all_subsets(elements, *args):
    rng = range(*args) if len(args) else range(0, len(elements) + 1)
    return chain(*map(lambda x: combinations(elements, x), rng))


def zero_row(row):
    return all(el == 0 for el in row)


def gen_gaussian_rec(es, col_num, row_num, stack, zeros):
    indices = set(range(len(es))) - stack

    row_set = []
    for row_idx in indices:
        if es[row_idx][col_num] == 1 and all(el == 0 for el in es[row_idx][:col_num]):
            row_set.append(row_idx)

    for row_subset in all_subsets(row_set, 1, len(row_set) + 1, 2):
        sum_rows(es[row_num], *[es[r] for r in row_subset])
        stack = stack.union(row_subset)

        if all(el == 0 for el in es[row_num]):
            for zero_subset in all_subsets(zeros):
                yield tuple(stack) + zero_subset

        if any(el == 1 for el in es[row_num]):
            col_num_rec = col_num
            while es[row_num][col_num_rec] == 0:
                col_num_rec += 1

            yield from gen_gaussian_rec(es, col_num_rec, row_num, stack, zeros)

        sum_rows(es[row_num], *[es[r] for r in row_subset])
        stack = stack.difference(row_subset)


def gen_gaussian(es_r):
    es = copy.deepcopy(es_r)
    numbers = set()
    zeros = list(filter(lambda rr: zero_row(es[rr]), range(len(es))))
    for subset in all_subsets(zeros, 1, len(zeros) + 1):
        yield subset
    for idx, row in enumerate(es):
        if idx in zeros:
            continue
        idx_1 = 0
        while row[idx_1] == 0:
            idx_1 += 1
        numbers.add(idx)
        yield from gen_gaussian_rec(es, idx_1, idx, numbers, zeros)
        numbers.remove(idx)


def method(n, base):
    print('База:', base)
    h = len(base) - 1

    ps = []
    alphas = []
    es = []

    sf = gen_suitable_fractions(n)

    while len(ps) < h + 2:
        try:
            pi = next(sf)
        except ValueError:
            return None

        pi2 = pi ** 2 % n
        if n - pi2 < pi2:
            pi2 = -(n - pi2)
        smooth, alpha, e = is_b_smooth(pi2, base)
        if smooth:
            ps.append(pi)
            alphas.append(alpha)
            es.append(e)

    for ks in gen_gaussian(es):
        s = 1
        for k in ks:
            s = (s * ps[k]) % n
        t = 1
        for b_idx, b in enumerate(base):
            t = (t * pow(b, functools.reduce(int.__add__, (alphas[k][b_idx] for k in ks)) // 2, n)) % n
        assert pow(s, 2, n) == pow(t, 2, n)

        if s != t and s != n - t:
            p = gcd((s - t) % n, n)
            return p



