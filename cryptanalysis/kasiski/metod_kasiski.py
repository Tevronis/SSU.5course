import collections
import math


def nod(mas):
    if len(mas) == 1:
        return mas[0]
    return math.gcd(mas[0], nod(mas[1:]))


def get_substrings(length):
    result = collections.Counter()
    with open("crypt.txt", 'r') as fin:
        text = fin.read()
    for i in range(0, len(text) - length + 1):
        result[text[i: i + length]] += 1
    ans = set()
    for k, v in result.items():
        if v > 2:
            mas = []
            tmp = None
            while tmp != -1:
                if tmp is None:
                    previous = text.find(k, 0)
                    tmp = previous
                tmp = text.find(k, tmp + 1)
                if tmp != -1:
                    mas.append(tmp-previous)
                    previous = tmp
            NOD = nod(mas)
            ans.add(NOD)
    return ans
