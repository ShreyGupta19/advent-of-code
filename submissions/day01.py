from advent import AdventProblem


def part_1(numbers):
    for n1 in numbers:
        for n2 in numbers:
            if n1 + n2 == 2020:
                return n1 * n2


def part_2(numbers):
    for n1 in numbers:
        for n2 in numbers:
            for n3 in numbers:
                if n1 + n2 + n3 == 2020:
                    return n1 * n2 * n3


if __name__ == '__main__':
    part1 = AdventProblem(1, 1, lambda l: int(l))
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(1, 2, lambda l: int(l))
    part2.add_solution(part_2)
    part2.run()
