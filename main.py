import argparse
from tools import tools
from toolsets import toolset
from primes import primes
import timeit

class NumberGenerator:
    def __init__(self, seed, increments, n=0):
        self._len = len(increments)
        self.seed = seed
        self.increments = increments
        if n == 0:
            self.round = 0
            self.index = 0
        else:
            self.round = n // self._len
            self.index = n % self._len

    def next_number(self):
        value = self.seed[self.index] + self.round * self.increments[self.index]
        self.index += 1
        if self.index == self._len:
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
        # print("Number is divisible by 2")
        return
    elif three_test(T_str):
        # print("Number is divisible by 3")
        return
    elif five_test(T_str):
        # print("Number is divisible by 5")
        return
    else:
        new_T = float(T) / 48
        T_str = truncate(new_T, 2)
        os, ts = T_str.split(".")
        up, down, delta = toolset[ts].split(",")

        os = int(os) + int(delta)
        us, ui, ufunc = tools[up]
        ds, di, dfunc = tools[down]

        cycles = 0
        total_iterations = 0
        up_iters = 0
        down_iters = 0

        up_gen = NumberGenerator(us, ui)
        down_gen = NumberGenerator(ds, di)

        while os != 0:
            while os > 0:
                down = down_gen.next_number()
                os -= down
                down_iters += 1
            while os < 0:
                up = up_gen.next_number()
                os += up
                up_iters += 1
            cycles += 1

        down = dfunc([down_gen.next_number() for _ in range(len(ds))])
        up = ufunc([up_gen.next_number() for _ in range(len(us))])
        F1 = down - up
        F2 = down + up
        if F2 == T:
            total_iterations = up_iters + down_iters
            # print("Prime", up_iters, down_iters, T)
            return True
        else:
            # print("Not Prime", up_iters, down_iters, T, )
            return False


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def closed_form(seed, increment, n):
    """
    find the nth term of a tool series, given the starting values (seed) and the increment values
    """
    _len = len(seed)
    rounds = n // _len  # flat divide
    remainder = n % _len  # modulo
    ns = [rounds for _ in range(_len)]
    for i in range(remainder):
        ns[i] += 1
    _sum = 0
    for i in range(_len):
        _sum += (ns[i] * seed[i]) + increment[i] * ((ns[i] * (ns[i] - 1)) / 2)
    return _sum


def v2(T):
    T_str = str(T)
    if two_test(T_str) or three_test(T_str) or five_test(T_str):
        # print(T, "is not prime")
        return False
    else:
        new_T = float(T) / 48
        T_str = truncate(new_T, 2)
        os, ts = T_str.split(".")
        up, down, delta = toolset[ts].split(",")
        os = int(os) + int(delta)

        us, ui, ufunc = tools[up]
        ds, di, dfunc = tools[down]

        total_iterations = T // 8
        base = total_iterations // 3

        for of1 in [0, 1]:
            for of2 in [0, 1]:
                if closed_form(us, ui, (base * 2) + of1) - closed_form(ds, di, base + of2) == -os:
                    up_start = (base * 2) + of1
                    down_start = base + of2
                    if stage_two(T, up_start, down_start):
                        print(T, "is prime")
                        return True
                    else:
                        print(T, "is not prime")
                        return False
                elif closed_form(us, ui, base + of1) - closed_form(ds, di, (base * 2) + of2) == -os:
                    up_start = base + of1
                    down_start = (base * 2) + of2
                    if stage_two(T, up_start, down_start):
                        print(T, "is prime")
                        return True
                    else:
                        print(T, "is not prime")
                        return False
        print(T, "is not prime")
        return False


def stage_two(T, up_start, down_start):
    new_T = float(T) / 48
    T_str = truncate(new_T, 2)
    os, ts = T_str.split(".")
    up, down, delta = toolset[ts].split(",")

    os = int(os) + int(delta)
    us, ui, ufunc = tools[up]
    ds, di, dfunc = tools[down]

    max_iters = min(up_start, down_start)
    up_gen = NumberGenerator(us, ui)
    down_gen = NumberGenerator(ds, di)
    iters = 0
    while os != 0 and iters <= max_iters:
        while os > 0 and iters <= max_iters:
            down = down_gen.next_number()
            os -= down
            iters += 1
        while os < 0 and iters <= max_iters:
            up = up_gen.next_number()
            os += up
            iters += 1

    if os == 0 and iters < max_iters:
        return False
    else:
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integer', type=int, help='an integer that may or may not be prime')

    args = parser.parse_args()

    v2(args.integer)
    # for prime in primes[10000:]:
    #     argyle_prime(prime)



