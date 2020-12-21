import functools
from collections import Counter

from advent import AdventProblem


def part_1(joltages):
    joltages = sorted(joltages)
    differences = [j2 - j1 for j1, j2 in zip(joltages[:-1], joltages[1:])]
    dist = Counter(differences)
    return (1 + dist[1]) * (1 + dist[3])

def part_2(joltages):
    joltages = set(joltages)
    target = max(joltages)

    @functools.lru_cache(maxsize=1024)
    def count_charge_paths(curr):
        if curr == target:
            return 1
        total = 0
        for i in range(1, 4):
            if (curr + i) in joltages:
                total += count_charge_paths(curr + i)
        return total
    return count_charge_paths(0)


if __name__ == '__main__':
    part1 = AdventProblem(10, 1, int)
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(10, 2, int)
    part2.add_solution(part_2)
    part2.run()
