import argparse
import json
import sys

from protocols.hughes import Hughes


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


def create_public_params(protocol):
    public_params = protocol.get_public_params()
    with open('public_params.dat', 'w') as f:
        json.dump(public_params, f, indent=True)


def create_private_params(protocol, users):
    for user in users:
        print('>> Generating params to user "{}"'.format(user))
        private_params = protocol.get_private_params('public_params.dat')
        with open(user + '.sec', 'w') as f:
            json.dump(private_params, f)


def start_protocol(protocol, users, initiator):
    users_dict = {}
    with open('public_params.dat', 'r') as f:
        public_params = json.load(f)
    for user in users:
        users_dict[user] = protocol(user, public_params)

    protocol.run(users_dict, initiator)


def main():
    # 1 - create public params, 2 - create private params, 3 - start protocol
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=int, default=1)
    parser.add_argument('-p', type=str)
    args = parser.parse_args(sys.argv[1:])

    protocol = str_to_class(args.p)

    if args.m == 1:
        create_public_params(protocol)
    elif args.m == 2:
        users = input('Please, enter users names: ').split()
        create_private_params(protocol, users)
    elif args.m == 3:
        users = input('Please, enter users names: ').split()
        print('User {} is initiator'.format(users[0]))
        start_protocol(protocol, users, users[0])
    #input()


if __name__ == '__main__':
    # sys.stdout = open('log.log', 'w')
    main()
