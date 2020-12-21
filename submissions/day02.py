import re

from advent import AdventProblem


def preprocess(line):
    match = list(re.match(r'(\d+)-(\d+) ([a-z]): (\w+)', line.strip()).groups())
    match[0] = int(match[0])
    match[1] = int(match[1])
    return tuple(match)


def part_1(passwords):
    valid = 0
    for (min_occur, max_occur, key_letter, password) in passwords:
        if min_occur <= password.count(key_letter) <= max_occur:
            valid += 1
    return valid


def part_2(passwords):
    valid = 0
    for (pos_a, pos_b, key_letter, password) in passwords:
        if (password[pos_a - 1] == key_letter) ^ (password[pos_b - 1] == key_letter):  # xor
            valid += 1
    return valid


if __name__ == '__main__':
    part1 = AdventProblem(2, 1, preprocess)
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(2, 2, preprocess)
    part2.add_solution(part_2)
    part2.run()
