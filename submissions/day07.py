import re
from collections import defaultdict

from advent import AdventProblem


def preprocess(line):
    match = re.match(r"([\w\s]+) bags contain (.+)\.", line)
    constituents = re.findall(r"(\d+) ([\w\s]+) bags?", match.group(2))
    return (match.group(1), constituents)

def part_1(pairings):
    contained_by = defaultdict(list)
    for bag, constituents in pairings:
        for n, c in constituents:
            contained_by[c].append(bag)

    num_bags = 0
    bags_to_visit = ["shiny gold"]
    visited = set()
    while len(bags_to_visit) > 0:
        curr_bag = bags_to_visit.pop()
        if curr_bag in visited:
            continue
        visited.add(curr_bag)
        num_bags += 1
        bags_to_visit += contained_by[curr_bag]
    return num_bags - 1


def part_2(pairings):
    contains = {}
    for bag, constituents in pairings:
        contains[bag] = [(c, int(n)) for n, c in constituents]

    num_bags = 0
    bags_to_open = [("shiny gold", 1)]
    while len(bags_to_open) > 0:
        bag, mult = bags_to_open.pop()
        num_bags += mult
        bags_to_open += [(c, n * mult) for c, n in contains[bag]]
    return num_bags - 1


if __name__ == '__main__':
    part1 = AdventProblem(7, 1, preprocess)
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(7, 2, preprocess)
    part2.add_solution(part_2)
    part2.run()
