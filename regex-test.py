
from pprint import pprint
import re
import sys

regex = r'\w+'


def main():
    args = sys.argv
    args.remove(__file__)

    if len(args) < 1:
        print('requires at least one input argument')
        exit(1)

    success = {}
    for i in range(0, len(args)):
        result = re.match(regex, args[i])
        if result:
            success.update({result.string: result.group()})
            print('.', end='')
            continue

        print('x', end='')
    else:
        print('\n\r')

    print(f'matched {len(success):02d}/{len(args):02d}')

    excluded = set(args).difference(success.keys())
    if (excluded):
        print(f'failed to match {excluded}')

    if success:
        print('\n\rresults')
        for key in success:
            print(f'{key}: {success[key]}')


if __name__ == '__main__':
    main()
