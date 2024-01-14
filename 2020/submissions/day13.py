import math
import operator
from functools import reduce

from advent import AdventProblem


def preprocess(lines):
    time = int(lines[0])
    buses = [(i, int(x)) for i, x in enumerate(lines[1].split(',')) if x != 'x']
    return time, buses


def part_1(inputs):
    time, buses = inputs
    buses = [b[1] for b in buses]
    elapsed, best = min([(math.ceil(time / bus) * bus - time, bus) for bus in buses],
            key=operator.itemgetter(0))
    return elapsed * best

# Copied from rosetta code
def chinese_remainder(n, a):
    def mul_inv(a, b):
        b0 = b
        x0, x1 = 0, 1
        if b == 1: return 1
        while a > 1:
            q = a // b
            a, b = b, a%b
            x0, x1 = x1 - q * x0, x0
        if x1 < 0: x1 += b0
        return x1

    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def part_2(inputs):
    time, buses = inputs
    modulos = [b[1] for b in buses]
    remainders = [b[1] - b[0] for b in buses]
    return chinese_remainder(modulos, remainders)


if __name__ == '__main__':
    part1 = AdventProblem(13, 1, preprocess, 'file')
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(13, 2, preprocess, 'file')
    part2.add_solution(part_2)
    part2.run()
