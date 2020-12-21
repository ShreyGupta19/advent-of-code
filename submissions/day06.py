from collections import Counter

from advent import AdventProblem


def preprocess(lines):
    groups = []
    group = []
    for l in lines:
        if len(l) == 0:
            groups.append(group)
            group = []
        else:
            group.append(l)
    if len(group) > 0:
        groups.append(group)
    return groups


def part_1(groups):
    num_yes = 0
    for group in groups:
        num_yes += len(set(''.join(group)))
    return num_yes


def part_2(groups):
    num_yes = 0
    for group in groups:
        for k, v in Counter(''.join(group)).items():
            if v == len(group):
                num_yes += 1
    return num_yes


if __name__ == '__main__':
    part1 = AdventProblem(6, 1, preprocess, "file")
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(6, 2, preprocess, "file")
    part2.add_solution(part_2)
    part2.run()
