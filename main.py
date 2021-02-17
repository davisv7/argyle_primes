import argparse
from tools import tools
from toolsets import toolset
from primes import primes


class NumberGenerator:
    def __init__(self, seed, increments):
        self._len = len(increments)
        self.seed = seed
        self.increments = increments
        self.round = 0
        self.index = 0

    def next_number(self):
        _len = len(self.increments)
        value = self.seed[self.index] + self.round * self.increments[self.index]
        self.index += 1
        if self.index == _len:
            self.round += 1
            self.index = 0
        return value


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d + '0' * n)[:n]])


def two_test(T_str):
    return int(T_str[-1]) in [0, 2, 4, 6, 8]


def three_test(T_str):
    x = sum(map(int, T_str))
    while x > 10:
        x = str(x)
        x = sum(map(int, x))
    return x in [3, 6, 9]


def five_test(T_str):
    return int(T_str[-1]) == 5


def argyle_prime(T):
    T_str = str(T)
    if two_test(T_str):
        print("Number is divisible by 2")
        return
    elif three_test(T_str):
        print("Number is divisible by 3")
        return
    elif five_test(T_str):
        print("Number is divisible by 5")
        return
    else:
        new_T = float(T) / 48
        T_str = truncate(new_T, 2)
        os, ts = T_str.split(".")
        os = int(os)
        up, down, delta = toolset[ts].split(",")
        us, ui, ufunc = tools[up]
        ds, di, dfunc = tools[down]

        up_gen = NumberGenerator(us, ui)
        down_gen = NumberGenerator(ds, di)

        os += int(delta)
        while os != 0:
            while os > 0:
                down = down_gen.next_number()
                os -= down
            while os < 0:
                up = up_gen.next_number()
                os += up

        down = dfunc([down_gen.next_number() for _ in range(len(ds))])
        up = ufunc([up_gen.next_number() for _ in range(len(us))])
        F1 = down - up
        F2 = down + up
        if F2 == T:
            print(T, "is Prime")
        else:
            print(T, "Something went wrong", )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integer', type=int, help='an integer that may or may not be prime')

    args = parser.parse_args()

    argyle_prime(args.integer)
    # for prime in primes:
    #     argyle_prime(prime)
