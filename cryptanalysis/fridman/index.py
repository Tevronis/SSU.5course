import random
import collections


def overlap_index(a, b):
    N = len(a)
    I = 0
    for i in range(N):
        if a[i] == b[i]:
            delta = 1
        else:
            delta = 0
        I += delta
    I = I/N
    return I


def average_overlap_index(a, b, alf):
    N = len(a)
    I = 0
    count_a = collections.Counter()
    count_b = collections.Counter()
    for i in range(len(a)):
        count_a[a[i]] += 1
        count_b[b[i]] += 1
    for i in range(len(alf)):
        I += (count_a[alf[i]]/N)*(count_b[alf[i]]/N)
    return I


