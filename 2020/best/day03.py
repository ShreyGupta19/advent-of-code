import functools
import operator

from utils import timed


def parse(file):
    with open(file) as f:
        replacements = {
            ".": False,
            "#": True,
        }
        return [[replacements[ch] for ch in line.strip()] for line in f]


def count_trees_encountered(map, r_step, c_step):
    r, c = 0, 0
    rows, cols = len(map), len(map[0])
    tree_count = 0
    while r < rows - r_step:
        c = (c + c_step) % cols
        r += r_step
        if map[r][c]:
            tree_count += 1
    return tree_count


@timed(3, 1)
def part_1(map):
    """
    Absolute cake walk: just step through the array.
    """
    return count_trees_encountered(map, 1, 3)


@timed(3, 2)
def part_2(map):
    """
    Evaluate `count_trees_encountered` in a loop with the different steps.
    """
    steps = [
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1)
    ]
    trees = [count_trees_encountered(map, r, c) for r, c in steps]
    return functools.reduce(operator.mul, trees, 1)


if __name__ == '__main__':
    inputs = parse('../inputs/3.txt')
    part_1(inputs)
    part_2(inputs)
