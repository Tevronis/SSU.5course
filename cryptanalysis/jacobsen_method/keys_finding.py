import random
import vigenere
import matrix


def get_random_key(d, alf):
    key = ''
    for i in range(d):
        tmp = random.randint(0, len(alf)-1)
        key += alf[tmp]
    return key


def objective_function(mx, current_mx):
    result = 0
    for i in range(len(mx)):
        for j in range(len(mx)):
            result += abs(current_mx[i][j] - mx[i][j])
    return result


def change_key(key, pos, num, alf):
    result = ''
    for i in range(len(key)):
        if i != pos:
            result += key[i]
        else:
            result += alf[num]
    return result


def best_key(key, pos, mx, w_func, alf, crypt):
    best_char = 0
    for i in range(len(alf)):
        key = change_key(key, pos, i, alf)
        text = vigenere.vigenere_decryption(crypt, key, alf)
        current_mx = matrix.get_reference_matrix(text, alf)
        new_w_func = objective_function(mx, current_mx)
        if new_w_func <= w_func:
            w_func = new_w_func
            best_char = i
    key = change_key(key, pos, best_char, alf)
    return key, w_func


def finding_best_key(d, mx, w_func, alf, crypt, key):
    for i in range(d):
        key, w_func = best_key(key, i, mx, w_func, alf, crypt)
    return key, w_func


def finding(d, alf, crypt, mx):
    key = get_random_key(d, alf)
    text = vigenere.vigenere_decryption(crypt, key, alf)
    current_mx = matrix.get_reference_matrix(text, alf)
    w_func = objective_function(mx, current_mx)

    new_key = key
    print(new_key)
    new_key, w_func = finding_best_key(d, mx, w_func, alf, crypt, new_key)

    while new_key != key:
        print(new_key)
        key = new_key
        new_key, w_func = finding_best_key(d, mx, w_func, alf, crypt, new_key)
    return key
