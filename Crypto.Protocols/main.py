import random
import sympy

def getBigDigit(a=1000000, b=1000000000):
    return random.randint(a, b)

def getGN():
    sympy.randprime()


def main():
    users = input('Please enter users name (2 or more): ').split()
    print('User {} is main user'.format(users[0]))

    pass

if __name__ == '__main__':
    main()