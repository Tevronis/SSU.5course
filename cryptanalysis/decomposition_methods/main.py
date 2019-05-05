from math import sqrt

import rsa_indexes
import rsa_params
import rsa_phi
import trial_division
import ro_pollard
import pminus1_pollard
import square_method
import prime_test
import gen_base
import Dixon


# Пробное деление
def trial_division_mode():
    mod1 = int(input('1 - создание базы\n'
                     '2 - метод пробного деления\n> '))
    if mod1 == 1:
        base = list(map(int, open('base.txt', 'r').read().split()))
        t = int(input('Введите t: '))
        ans = trial_division.make_base(base, t)
        with open('trial_base.txt', 'w') as fout:
            for item in ans:
                fout.write(str(item) + ' ')
        print('Сгенерированная база:', ans)
        print('Сохранен файл trial_base.txt')

    if mod1 == 2:
        base = list(map(int, open('base.txt', 'r').read().split()))
        trial_base = list(map(int, open('trial_base.txt', 'r').read().split()))
        n = int(input('Введите нечетное число: '))
        assert n % 2 != 0, "Четное число"
        assert not prime_test.miller_rabin(n), "Простое число"
        assert sqrt(n) <= trial_base[len(trial_base) - 1], "Недостаточная база"

        ans = trial_division.decomposition(n, base, trial_base)
        ans = sorted(ans)
        print(ans)
        with open('Ответ для пробного деления.txt', 'w') as fout:
            for item in ans:
                fout.write(str(item) + ' ')
        print('Сохранен файл Ответ для пробного деления.txt')


# p-метод Полларда
def ro_pollard_mode():
    n = int(input('Введите нечетное число: '))
    c = int(input('Введите начальное значение c (1 <= c < n): '))
    assert 1 <= c < n
    # print('f(x) = x^p + s (mod n)')
    # p = int(input('Введите p = '))
    # s = int(input('Введите s = '))
    # ans = ro_pollard.method(n, c, p, s)
    ans = ro_pollard.method(n, c, 2, 1)
    print(ans)
    with open('Ответ для p-поллард.txt', 'w') as fout:
        fout.write(str(ans))
    print('Сохранен файл Ответ для p-поллард.txt')


def pminus1_pollard_mode():
    base_len = int(input('Введите длину базы: '))
    base = gen_base.make_base(base_len)
    n = int(input('Введите нечетное число: '))
    ans = pminus1_pollard.method(n, base)
    print(ans)
    with open('Ответ для (p-1)поллард.txt', 'w') as fout:
        fout.write(str(ans))
    print('Сохранен файл Ответ для (p-1)поллард.txt')


def square_method_mode():
    n = int(input('Введите большое натуральное число: '))
    k = int(input('Введите коэффициент близости (1, 2, 3, .., 10, ..): '))
    l = int(input('Число итераций: '))
    cnt = l
    ans = square_method.ferma(n, k, l, 1)
    if ans == -1:
        say = input('Попробовать еще {} раз? [y/n]: '.format(cnt))
        while say == 'y':
            start = l
            l += l
            ans = square_method.ferma(n, k, l, start)
            if ans == -1:
                say = input('Попробовать еще {} раз? [y/n]: '.format(cnt))
            else:
                say = 'no'
    print(ans)
    with open('Ответ для метод квадратов.txt', 'w') as fout:
        fout.write(str(ans))
    print('Сохранен файл Ответ для метод квадратов.txt')


def dixon_mode():
    n = int(input('Введите составное число: '))
    base = gen_base.make_base_dixon(n)
    ans = Dixon.method(n, base)
    print('Ответ:', ans)
    with open('Ответ для метода Диксона.txt', 'w') as fout:
        fout.write(str(ans))
    print('Сохранен файл Ответ для метода Диксона.txt')


def rsa_mode():
    rsa_params.gen_params()


def rsa_phi_mode():
    x1, x2 = rsa_phi.decomposition()
    print('x1: {}, x2: {}'.format(x1, x2))


def rsa_indexes_mode():
    p, q = rsa_indexes.decomposition()
    print('p: {}, q: {}'.format(p, q))


def main():
    # ‭35438707‬
    # 35438707 = 6359 * 5573
    mod = int(input('0 - генерация базы простых чисел\n'
                    '1 - метод пробного деления\n'
                    '2 - метод po-полларда\n'
                    '3 - метод (p-1)-полларда\n'
                    '4 - метод квадратов\n'
                    '5 - метод Диксона\n'
                    '6 - вычисление параметров RSA\n'
                    '7 - разложение по известному значению ф. Эйлера\n'
                    '8 - разложение по известным показателям RSA\n> '))

    if mod == 0:
        l = int(input('Введите необходимую длину базы: '))
        base = gen_base.make_base(l)
        with open('base.txt', 'w') as fout:
            for item in base:
                fout.write(str(item) + ' ')
        print('Сохранен файл base.txt')

    if mod == 1:
        trial_division_mode()

    if mod == 2:
        ro_pollard_mode()

    if mod == 3:
        pminus1_pollard_mode()

    if mod == 4:
        square_method_mode()

    if mod == 5:
        dixon_mode()

    if mod == 6:
        rsa_mode()

    if mod == 7:
        rsa_phi_mode()

    if mod == 8:
        rsa_indexes_mode()


if __name__ == '__main__':
    main()
