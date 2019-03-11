import collections
import time

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


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x


# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


def gauss(n, system, m, changable):
    for i in range(n):
        if i < n:
            if system[i][i] == 0:
                change_matrix(system, changable, i, i)
            else:
                changable.remove(i)
            elem = system[i][i]
            if elem != 1:
                obr_elem = mulinv(elem, m)
                for j in range(len(system[i])):
                    system[i][j] *= obr_elem
                    system[i][j] %= m
            for k in range(i + 1, n):
                mult = system[k][i]
                mult = -mult
                for a in range(len(system[i])):
                    system[k][a] += mult * system[i][a]
                    system[k][a] %= m
            if i != 0:
                for k in range(0, i):
                    mult = system[k][i]
                    mult = -mult
                    for a in range(len(system[i])):
                        system[k][a] += mult * system[i][a]
                        system[k][a] %= m
            for j in range(n):
                c = collections.Counter(system[j])
                if c[0] == len(system[j]):
                    system.remove(system[j])
                    n -= 1
        not_solved(system)
    return system



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
    start = time.time()
    for i in range(100000):
        changable = [i for i in range(n)]
        gauss(n, system, m, changable)
    print(time.time() - start)
    '''
    for i in range(len(ans_system)):
        for j in range(len(ans_system[i])):
            if ans_system[i][j] != 0:
                if j < len(ans_system[i]) - 2:
                    print("(" + str(ans_system[i][j]) + "x" + str((j+1)) + ") + ", end="")
                elif j == len(ans_system[i]) - 2:
                    print("(" + str(ans_system[i][j]) + "x" + str(j + 1) + ") ", end="")
                elif j == len(ans_system[i]) - 1:
                    print(" = (" + str(ans_system[i][j]) + ")")
            if ans_system[i][j] == 0 and j == len(ans_system[i]) - 1:
                    print(" = (" + str(ans_system[i][j]) + ")")
    '''


if __name__ == '__main__':
    main()

