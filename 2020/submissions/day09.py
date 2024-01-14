from advent import AdventProblem


def sum_pair(numbers, sum_to):
    """
    Naive approach with double for loop over unsorted numbers array
    Complexity: O(n2)
    """
    for n1 in numbers:
        for n2 in numbers:
            if n1 + n2 == sum_to:
                return True
    return False


def part_1(nums, preamble_len=25):
    context = nums[:preamble_len]
    for n in nums[preamble_len:]:
        if not sum_pair(context, n):
            return n
        else:
            context = context[1:] + [n]


def part_2(nums):
    TARGET = 133015568
    for i in range(2, len(nums)):
        for j in range(len(nums) - i):
            if sum(n for n in nums[j:j+i]) == TARGET:
                return min(nums[j:j+i])+max(nums[j:j+i])


if __name__ == '__main__':
    part1 = AdventProblem(9, 1, int)
    part1.add_solution(part_1)
    part1.run()

    part2 = AdventProblem(9, 2, int)
    part2.add_solution(part_2)
    part2.run()
