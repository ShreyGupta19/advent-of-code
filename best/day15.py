from collections import defaultdict

from utils import timed


def parse(file):
    with open(file) as f:
        return [int(x) for x in f.read().split(',')]


def play_memory_game(starting_nums, num_turns):
    occurrences = defaultdict(list)
    for i, s in enumerate(starting_nums):
        occurrences[s].append(i)

    last_num = starting_nums[-1]
    for i in range(len(starting_nums), num_turns):
        try:
            last_num = occurrences[last_num][-1] - occurrences[last_num][-2]
        except IndexError:
            last_num = 0
        occurrences[last_num].append(i)
    return last_num


@timed(15, 1)
def part_1(starting_nums):
    """
    We use a defaultdict to maintain the occurrences of each number. Since the lists in this dict
    get arbitrarily large, we abstain from calling len on these lists to see if a number has
    occurred more than once. Instead, we just assume there's > 1 occurrence, and use an except
    block to handle the case where there is just 1 occurrence. This saves an enormous amount of time
    on useless O(n) len calls.
    """
    return play_memory_game(starting_nums, 2020)


@timed(15, 2)
def part_2(starting_nums):
    """
    Same thing, just more turns.
    """
    return play_memory_game(starting_nums, 30000000)


if __name__ == '__main__':
    inputs = parse('../inputs/15.txt')
    part_1(inputs)
    part_2(inputs)
