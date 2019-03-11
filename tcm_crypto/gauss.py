import collections

import utils


def change_matrix(system, changable, id_column, id_string):
    for i in range(len(system)):
        if system[i][id_column] != 0 and i in changable:
            system[i], system[id_string] = system[id_string], system[i]
            changable.remove(id_string)
            break


def not_solved(system):
    for i in range(len(system)):
        c = collections.Counter(system[i][:-1])
        if c[0] == len(system[i]) - 1 and system[i][-1] != 0:
            print("Нет решений")
            exit(0)


# System of linear equations
def gauss(n, SOLE, m, changable):
    for i in range(n):
        if i < n:
            if SOLE[i][i] == 0:
                change_matrix(SOLE, changable, i, i)
            else:
                changable.remove(i)
            elem = SOLE[i][i]
            if elem != 1:
                obr_elem = utils.inverse(elem, m)
                for j in range(len(SOLE[i])):
                    SOLE[i][j] *= obr_elem
                    SOLE[i][j] %= m
            for k in range(i + 1, n):
                mult = SOLE[k][i]
                mult = -mult
                for a in range(len(SOLE[i])):
                    SOLE[k][a] += mult * SOLE[i][a]
                    SOLE[k][a] %= m
            if i != 0:
                for k in range(0, i):
                    mult = SOLE[k][i]
                    mult = -mult
                    for a in range(len(SOLE[i])):
                        SOLE[k][a] += mult * SOLE[i][a]
                        SOLE[k][a] %= m
            for j in range(n):
                c = collections.Counter(SOLE[j])
                if c[0] == len(SOLE[j]):
                    SOLE.remove(SOLE[j])
                    n -= 1
        not_solved(SOLE)
    return SOLE


def main():
    system = []
    n = int(input("Введите количество уравнений в системе: "))
    m = int(input("Введите модуль: "))
    for i in range(n):
        equation = list(map(int, input().split()))
        system.append(equation)
    changable = [i for i in range(n)]
    for i in range(len(system)):
        for j in range(len(system[i])):
            system[i][j] %= m
    ans_system = gauss(n, system, m, changable)
    ans = []
    for i in range(len(ans_system)):
        aa = []
        for j in range(len(ans_system[i])):
            if ans_system[i][j] != 0:
                if j <= len(ans_system[i]) - 2:
                    if ans_system[i][j] == 1:
                        aa.append("x{}".format(j + 1))
                    else:
                        aa.append("({})*x{}".format(ans_system[i][j], j + 1))
                elif j == len(ans_system[i]) - 1:
                    aa.append(" = {}".format(ans_system[i][j]))
            if ans_system[i][j] == 0 and j == len(ans_system[i]) - 1:
                aa.append(" = {}".format(ans_system[i][j]))
        ans.append(aa)
    for item in ans:
        print(' + '.join(item[:-1]), end='')
        print(item[-1])


if __name__ == '__main__':
    main()
