import re

from utils import timed


def parse(file):
    password_reqs = []
    with open(file) as f:
        for line in f:
            match = list(re.match(r'(\d+)-(\d+) ([a-z]): (\w+)', line.strip()).groups())
            match[0] = int(match[0])
            match[1] = int(match[1])
            password_reqs.append(tuple(match))
    return password_reqs


@timed(2, 1)
def part_1(passwords):
    """
    Absolute cake walk: just do a linear search on each password to count # of occurences.
    """
    valid = 0
    for (min_occur, max_occur, key_letter, password) in passwords:
        if min_occur <= password.count(key_letter) <= max_occur:
            valid += 1
    return valid


@timed(2, 2)
def part_2(passwords):
    """
    Ensure the target character appears in exactly one position using XOR.
    """
    valid = 0
    for (pos_a, pos_b, key_letter, password) in passwords:
        if (password[pos_a - 1] == key_letter) ^ (password[pos_b - 1] == key_letter):
            valid += 1
    return valid


if __name__ == '__main__':
    inputs = parse('../inputs/2.txt')
    part_1(inputs)
    part_2(inputs)
