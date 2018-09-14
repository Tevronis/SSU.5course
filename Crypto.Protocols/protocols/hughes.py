import json
import random
from math import gcd

import sympy
from protocols import *

import utils


class Hughes(Protocol):
    """
    Протокол Хьюза
    """

    def __init__(self, name, params):
        super().__init__(name, params)
        self.side = name
        self.x = None
        self.g = params['g']
        self.n = params['n']
        self.k = None
        self.z = None
        self.X = None
        self.Y = None
        self.users_keys = {}

    @staticmethod
    def get_public_params() -> dict:
        while True:
            n = utils.get_big_prime()
            if sympy.isprime((n - 1) // 2):
                break
        g = utils.generator(n)
        print('Сгенерированы параметры \n g: {} \n n: {}'.format(g, n))
        return {'g': g, 'n': n}

    @staticmethod
    def get_private_params(public_file) -> dict:
        with open(public_file) as f:
            public_params = json.load(f)

        while True:
            x = utils.get_big_digit()
            if gcd(x, public_params['n'] - 1) == 1 and utils.inverse(x, public_params['n'] - 1) >= 0:
                break

        z = utils.inverse(x, public_params['n'] - 1)  # None # Обратный элемент к self.x

        print("Сгенерирован открытый ключ x: {}".format(x))
        print("Вычислен параметр z (обратный элемент к x): {}".format(z))
        return {'x': x, 'z': z}

    def set_x(self):
        with open(self.side + '.sec') as f:
            data = json.load(f)
            self.x = data['x']
            self.z = data['z']

    @staticmethod
    def run(users_dict: dict, initiator):
        alice = users_dict.pop(initiator)
        bob = list(users_dict.values())[0]

        alice.set_x()
        bob.set_x()

        alice.create_param_k()  # k

        # Боб выбирает случайное большое целое число y и посылает Алисе Y = g^y mod n
        bob.create_param_Y()  # Y
        alice.add_user_key('bob', bob.Y)  # send to Alice

        # Алиса посылает бобу X = Y^x mod n
        alice.create_param_X('bob')  # X
        bob.add_user_key('alice', alice.X)  # send to Bob

        # Боб вычисляет z = y^-1 и k' = X^z mod n
        bob.create_secret_key('alice')  # создание общего ключа на основе данных Алисы

        if Hughes.compare_secrets_key(alice, bob):
            print('Ключи совпали {} {}'.format(alice.k, bob.k))
        else:
            print('Ключи не совпали {} {}'.format(alice.k, bob.k))
        pass

    def create_param_k(self):
        result = pow(self.g, self.x, self.n)
        print("Сгенерирован ключ k = {} пользователя {}".format(result, self.side))
        self.k = result

    def create_param_Y(self):
        result = pow(self.g, self.x, self.n)
        print("Сгенерирован ключ Y = {} для отправки собеседнику. Пользователем {}".format(result, self.side))
        self.Y = result

    def create_param_X(self, user):
        self.Y = self.users_keys[user]
        result = pow(self.Y, self.x, self.n)
        print("Сгенерирован ключ X = {} для отправки собеседнику. Пользователем {}".format(result, self.side))
        self.X = result

    def create_secret_key(self, user):
        X = self.users_keys[user]
        result = pow(X, self.z, self.n)
        print("Стороной {0} вычислен секретный ключ между пользователями {0} и {1}: {2}".format(self.side, user, result))
        self.k = result

    def add_user_key(self, user, key):
        self.users_keys[user] = key

    @staticmethod
    def compare_secrets_key(user1, user2):
        if user1.k == user2.k:
            open('TOP_SECRET_KEY.TXT', 'w').write(str(user1.k))
            return True
        return False
