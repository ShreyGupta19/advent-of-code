from collections import defaultdict
from tqdm import tqdm

from advent import AdventProblem


def preprocess(lines):
    return [int(x) for x in lines[0].split(',')]


def part_1(starting_nums, end=2020):
    nums = defaultdict(list)
    for i, s in enumerate(starting_nums):
        nums[s].append(i)

    last_num = starting_nums[-1]
    for i in tqdm(range(len(starting_nums), end)):
        if len(nums[last_num]) == 1:
            last_num = 0
        else:
            last_num = nums[last_num][-1] - nums[last_num][-2]
        nums[last_num].append(i)
    return last_num

def part_2(starting_nums):
    return part_1(starting_nums, 30000000)


if __name__ == '__main__':
    part1 = AdventProblem(15, 1, preprocess, "file")
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(15, 2, preprocess, "file")
    part2.add_solution(part_2)
    part2.run()
