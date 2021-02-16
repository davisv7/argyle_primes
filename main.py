import argparse
from tools import tools
from toolsets import toolset
from itertools import cycle
# from primes import primes


def make_generator(seed, increments):
    _len = len(increments)
    round = 0
    i = 0
    for digit in cycle(seed):
        yield digit + round * increments[i]
        i += 1
        if i == _len:
            round += 1
            i = 0


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
        new_T = T / 48
        T_str = truncate(new_T, 2)
        os, ts = T_str.split(".")
        os = int(os)
        up, down = toolset[ts].split(", ")
        us, ui, ufunc = tools[up]
        ds, di, dfunc = tools[down]
        # print(us, ui)
        # print(ds, di)
        up_gen = make_generator(us, ui)
        down_gen = make_generator(ds, di)
        # down = next(down_gen)
        # up = next(up_gen)
        while os != 0:
            while os > 0:
                down = next(down_gen)
                os -= down
            while os < 0:
                up = next(up_gen)
                os += up
        down = dfunc([next(down_gen) for i in range(len(ds))])
        up = ufunc([next(up_gen) for i in range(len(us))])
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
