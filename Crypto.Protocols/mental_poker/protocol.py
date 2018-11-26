import copy
import random
import sys

import sympy

import utils

colors_dict = {'1': 'buba', '2': 'baptize', '3': 'spades', '4': 'hearts'}
values_dict = {}


def create_deck():
    result = []
    colors = ['buba', 'kres', 'piki', 'cher']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'vale', 'lady', 'king', 'ace']
    for c in colors:
        for v in values:
            result.append(v + '_' + c)
    return result


def encrypt_cards(key, cards):
    result = []

    for card in cards:
        c = card
        if type(card) == str:
            # c = utils.str_to_digit(list(map(ord, card)))
            # print(card.encode('utf-8'))
            c = utils.str_to_digit(card.encode('utf-8'))
            # c = bytes(card, 'utf-8')
            # c = int.from_bytes(c, byteorder='big')
        result.append(pow(c, key[0], key[1]))

    return result


def choose_card(deck, cnt):
    ndeck = copy.copy(deck)
    result = []
    random.shuffle(ndeck)
    for i in range(cnt):
        result.append(ndeck.pop())

    return ndeck, result


def decrypt(key, cards):
    result = []

    for card in cards:
        c = pow(card, key[0], key[1])
        result.append(c)

    return result


def create_keys(cnt, l):
    result = []
    t = []
    n = sympy.randprime(2 ** (l - 1), 2 ** l)
    for i in range(cnt):
        e = random.randint(2, n - 1)
        while sympy.gcd(e, n - 1) != 1 and e not in t:
            e = random.randint(2, n - 1)
        t.append(e)
        d = utils.inverse(e, n - 1)
        result.append([[e, n], [d, n]])

    return result


if __name__ == '__main__':
    step = int(sys.argv[2])
    dont_crypt_deck = False
    if len(sys.argv) >= 5:
        dont_crypt_deck = int(sys.argv[4])
    debug = False
    if step == 1 or debug:  # Создают пары public/private
        l = utils.read_param('l.txt', 'l')
        A_keys, B_keys, C_keys = create_keys(3, l)
        utils.save_param('Alice/A_sk.json', 'key', A_keys[0])
        utils.save_param('A_ok.json', 'key', A_keys[1])
        utils.save_param('Bob/B_sk.json', 'key', B_keys[0])
        utils.save_param('B_ok.json', 'key', B_keys[1])
        utils.save_param('Carroll/C_sk.json', 'key', C_keys[0])
        utils.save_param('C_ok.json', 'key', C_keys[1])
    if step == 2 or debug:  # Alice step
        deck = create_deck()
        A_ok = utils.read_param('A_ok.json', 'key')
        if dont_crypt_deck:
            utils.save_param('Alice/deck52_not_crypted.json', 'deck', deck)
        edeck = encrypt_cards(A_ok, deck)
        utils.save_param('Alice/deck52.json', 'deck', edeck)
        utils.save_param('Bob/deck52.json', 'deck', edeck)
    if step == 3 or debug:  # Bob step
        deck = utils.read_param('Bob/deck52.json', 'deck')
        new_deck, cards = choose_card(deck, 5)
        B_ok = utils.read_param('B_ok.json', 'key')
        print('Ea(Bcards)\t\t', cards)
        ecards = encrypt_cards(B_ok, cards)
        print('Eb(Ea(Bcards))\t', ecards)
        utils.save_param('Alice/Bob_cards.json', 'cards', ecards)
        # step == 4
        utils.save_param('Carroll/deck47.json', 'deck', new_deck)
    if step == 5 or debug:  # Carroll
        deck = utils.read_param('Carroll/deck47.json', 'deck')
        new_deck, cards = choose_card(deck, 5)
        C_ok = utils.read_param('C_ok.json', 'key')
        print('Ea(Ccards)\t\t', cards)
        ecards = encrypt_cards(C_ok, cards)
        print('Ec(Ea(Ccards))\t', ecards)
        utils.save_param('Alice/Carroll_cards.json', 'cards', ecards)
        utils.save_param('Carroll/deck42.json', 'deck', new_deck)
    if step == 6 or debug:  # Alice
        B_cards = utils.read_param('Alice/Bob_cards.json', 'cards')
        C_cards = utils.read_param('Alice/Carroll_cards.json', 'cards')
        A_sk = utils.read_param('Alice/A_sk.json', 'key')
        print('Eb(Ea(Bcards))\t', B_cards)
        B_cards = decrypt(A_sk, B_cards)
        print('Da(Eb(Ea(Bcards))) = Eb(Bcards)\t', B_cards)
        print('Ec(Ea(Ccards))\t', C_cards)
        C_cards = decrypt(A_sk, C_cards)
        print('Da(Ec(Ea(Ccards))) = Ec(Ccards)\t', C_cards)
        utils.save_param('Bob/cards.json', 'cards', B_cards)
        utils.save_param('Carroll/cards.json', 'cards', C_cards)
    if step == 7 or debug:
        B_cards = utils.read_param('Bob/cards.json', 'cards')
        C_cards = utils.read_param('Carroll/cards.json', 'cards')
        B_sk = utils.read_param('Bob/B_sk.json', 'key')
        C_sk = utils.read_param('Carroll/C_sk.json', 'key')
        print('Eb(Bcards)\t\t', B_cards)
        B_cards = decrypt(B_sk, B_cards)
        print('Bcards\t\t', B_cards)
        print('Ec(Ccards)\t', C_cards)
        C_cards = decrypt(C_sk, C_cards)
        print('Ccards\t\t', C_cards)
        utils.save_param('Bob/cards.json', 'cards', utils.decode_utf8(B_cards))
        utils.save_param('Carroll/cards.json', 'cards', utils.decode_utf8(C_cards))
    if step == 8 or debug:  # Carroll
        deck = utils.read_param('Carroll/deck42.json', 'deck')
        new_deck, cards = choose_card(deck, 5)
        utils.save_param('Alice/cards.json', 'cards', cards)
    if step == 9 or debug:  # Alice
        A_sk = utils.read_param('Alice/A_sk.json', 'key')
        ecards = utils.read_param('Alice/cards.json', 'cards')
        print('Ea(Acards)\t', ecards)
        cards = decrypt(A_sk, ecards)
        print('Acards\t\t', cards)
        utils.save_param('Alice/cards.json', 'cards', utils.decode_utf8(cards))
