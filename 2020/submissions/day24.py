import re

import numpy as np
from tqdm import tqdm

from advent import AdventProblem


def minmax(iterable):
    iterator = iter(iterable)
    min = next(iterator)
    max = min
    for i in iterator:
        if i < min:
            min = i
        elif i > max:
            max = i
    return min, max

def preprocess(line):
    moves = re.findall('(?:sw)|(?:se)|(?:nw)|(?:ne)|w|e', line)
    return moves

MOVE_MAPPING = {
    'w': np.array([-1, 0]),
    'e': np.array([1, 0]),
    'nw': np.array([-0.5, 1]),
    'ne': np.array([0.5, 1]),
    'sw': np.array([-0.5, -1]),
    'se': np.array([0.5, -1]),
}

def part_1(movesets):
    flipped = set()
    for moveset in movesets:
        final_coord = tuple(sum([MOVE_MAPPING[m] for m in moveset]).tolist())
        if final_coord in flipped:
            flipped.remove(final_coord)
        else:
            flipped.add(final_coord)
    print(len(flipped))
    return flipped

def part_2(movesets):
    def get_neighbors(c):
        return [(c[0] + v[0], c[1] + v[1]) for v in MOVE_MAPPING.values()]

    black = part_1(movesets)
    for i in tqdm(range(100)):
        search_space = set(n for c in black for n in get_neighbors(c))
        new_black = set()
        for c in search_space:
            num_black = sum(n in black for n in get_neighbors(c))
            if c in black and (0 < num_black <= 2):
                new_black.add(c)
            elif c not in black and num_black == 2:
                new_black.add(c)
        black = new_black
    return len(black)

if __name__ == '__main__':
    part1 = AdventProblem(24, 1, preprocess)
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(24, 2, preprocess)
    part2.add_solution(part_2)
    part2.run()
