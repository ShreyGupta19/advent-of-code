import functools
import operator

from advent import AdventProblem


def preprocess(line):
    replacements = {
        ".": False,
        "#": True,
    }
    return [replacements[ch] for ch in line]


def part_1(map, x_step=3, y_step=1):
    x, y = 0, 0
    width = len(map[0])
    height = len(map)
    tree_count = 0
    while y < height - y_step:
        x = (x + x_step) % width
        y += y_step
        if map[y][x]:
            tree_count += 1
    return tree_count


def part_2(map):
    steps = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2)
    ]
    trees = [part_1(map, x, y) for x, y in steps]
    return functools.reduce(operator.mul, trees, 1)


if __name__ == '__main__':
    part1 = AdventProblem(3, 1, preprocess)
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(3, 2, preprocess)
    part2.add_solution(part_2)
    part2.run()
