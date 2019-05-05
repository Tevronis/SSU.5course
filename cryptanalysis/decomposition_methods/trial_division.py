import math
import prime_test


def make_base(base, t):
    k = int(input('Введите количество чисел: '))
    if k > len(base) // t:
        print('недостаточно простых чисел')
        exit()
    result = []
    cnt = 0
    for i in range(k):
        tmp = 1
        for j in range(t):
            tmp *= base[cnt+j]
        cnt += t
        result.append(tmp)
    return result


def decomposition(n, base, trial_base):
    ans = []
    bnum = 0
    while n not in base:
        d = math.gcd(trial_base[bnum], n)
        if d != 1:
            n = n // d
            if d in base:
                ans.append(d)
            else:
                tmp = 0
                while d not in base:
                        if d % base[tmp] == 0:
                            ans.append(base[tmp])
                            d = d // base[tmp]
                        else:
                            tmp += 1
                ans.append(d)
        else:
            if bnum+1 < len(trial_base):
                bnum += 1
            else:
                print('Не хватило базы!')
                exit()
    ans.append(n)
    return ans






