from utils import timed


def parse(file):
    with open(file) as f:
        return [int(l.strip()) for l in f]


def identify_sum_pair(numbers, sum_to):
    for n in numbers:
        comp_n = sum_to - n
        if sum_to - n in numbers:
            return n * comp_n
    return None


@timed(1, 1)
def part_1(numbers):
    """
    Use hashset to check for existence of complementary number in O(n) time.
    """

    return identify_sum_pair(set(numbers), 2020)


@timed(1, 2)
def part_2(numbers):
    """
    Loop over numbers list using hashset-based sum pair finder as subroutine.
    """
    numbers = set(numbers)
    for n1 in numbers:
        comp_sum = 2020 - n1
        res = identify_sum_pair(numbers - {n1}, sum_to=comp_sum)
        if res is not None:
            return n1 * res
    return None


if __name__ == '__main__':
    inputs = parse('../inputs/1.txt')
    part_1(inputs)
    part_2(inputs)
